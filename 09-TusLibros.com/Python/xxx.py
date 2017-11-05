# For python this file uses encoding: utf-8
import unittest
from collections import defaultdict
from datetime import date, timedelta, datetime
from copy import copy
from functools import partial
import random

class RESTInterface(object):

    EXPIRATED_CART_MSG = 'Expirated cart'
    INVALID_CREDENTIALS = 'Invalid credentials'
    INVALID_CART_ID = 'Not existing cart ID' 
    CART_INDEX = 0
    CLIENT_ID_INDEX = 1

    def __init__(self, users, catalog, clock, cart_ID_generator):
        self._users = users
        #cartID: (carro, clientID)
        self._cart_information_by_ID = {}
        self._catalog = catalog
        self._clock = clock
        self._sales_books = {}
        #esto no sabia como escribirlo mas corto
        for user in users.keys():
            self._sales_books[user] = []
        self._cart_ID_generator = cart_ID_generator

    def create_cart(self, client_ID, client_password):
        
        self.__check_valid_credentials__(client_ID, client_password)
        cart_ID = self._cart_ID_generator.new_ID()

        self._cart_information_by_ID[cart_ID]=(
                    ExpirableCart(
                        ShoppingCart(self._catalog),
                            timedelta(minutes=30),
                            self._clock
                        ),
                    client_ID
                    )

        return cart_ID

    def add_to_cart(self, cart_ID, book_ISBN, quantity):
        self.__check_valid_cart_ID__(cart_ID)
        self._cart_information_by_ID[cart_ID][self.__class__.CART_INDEX].add(book_ISBN, quantity)
         
    def list_cart(self, cart_ID):
        self.__check_valid_cart_ID__(cart_ID)
        return self._cart_information_by_ID[cart_ID][self.__class__.CART_INDEX].list()

    def checkout_cart(self, cart_ID, credit_card_number, card_expiration_date,
                      credit_card_owner):
        self.__check_valid_cart_ID__(cart_ID)
        a_cashier = Cashier()
        a_credit_card = CreditCard(credit_card_number, card_expiration_date, credit_card_owner)
        client_ID = self._cart_information_by_ID[cart_ID][self.__class__.CLIENT_ID_INDEX]
        a_cashier.check_out(
            cart = self._cart_information_by_ID[cart_ID][self.__class__.CART_INDEX],
            credit_card = a_credit_card,
            merchant_processor = MerchantProcessor(),
            date = self._clock.today(),
            client_sales_book = self._sales_books[client_ID]
            )

        #Decision de implementacion, la venta la guarda el cashier
        self._cart_information_by_ID.pop(cart_ID)

    def list_purchases(self, client_ID, client_password):
        self.__check_valid_credentials__(client_ID, client_password)
        return self._sales_books[client_ID]

    def __check_valid_credentials__(self, user, password):
        if (not user in self._users) or password != self._users[user]:          
            raise Exception(self.__class__.INVALID_CREDENTIALS)

    def __check_valid_cart_ID__(self, cart_ID):
        if not cart_ID in self._cart_information_by_ID.keys():
            raise Exception(self.__class__.INVALID_CART_ID)

class ExpirableCart(object):
    def __init__(self, a_shopping_cart, validity_time, clock):
        self._cart = a_shopping_cart
        self._last_use = clock.now()
        self._validity_time = validity_time
        self._clock = clock

    def __getattr__(self, attr):
        now = self._clock.now()
        if now - self._last_use < self._validity_time:
            self._last_use = now
            return getattr(self._cart, attr)
        else:
            raise Exception('Expirated cart')

class CartIDGenerator(object):
    #Para asegurarnos que no generamos de nuevo el mismo ID
    def __init__(self):
        self._generated_IDs = set()
    
    def new_ID(self):
        
        ID = ''.join(random.choice('0123456789ABCDEF') for i in range(16)) 
        
        if not ID in self._generated_IDs:
            return ID
        else: 
            return self.new_ID()

class RESTTests(unittest.TestCase):

    def setUp(self):
        self.juan_id = 'Juan'
        self.juan_password = 'password'
        self.users = {
            self.juan_id: self.juan_password
        }
        self.item_in_catalog = object()
        self.catalog = Catalog({self.item_in_catalog:10})
        self.interface = RESTInterface(self.users, self.catalog, self, CartIDGenerator())
        self.valid_cart_id = self.interface.create_cart(
            self.juan_id,
            self.juan_password
        )
        self.credit_card_number = 1234
        self.card_expiration_date = date.today()
        self.credit_card_owner = 'Tomas'

    def now(self):
        return datetime(
            year=2017,
            month=3,
            day=11
        ) 

    def today(self):
        return date.today()

    def test01_can_not_create_cart_with_invalid_username(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart('Pedro', self.juan_password)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )

        #Asertar que no se creo

    def test02_can_not_create_cart_with_invalid_password(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart(self.juan_id, 'invalid_password')

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )
        #asertar que no se creo 

    def test03_can_create_cart_with_valid_credentials(self):
        #esto para mi hay que revisarlo...

        self.assertEqual(len(self.interface.list_cart(self.valid_cart_id)), 0)

        
    def test04_can_not_add_items_to_an_expirated_cart(self):
        previous_datetime = self.now()

        def now(self):
            return previous_datetime + timedelta(minutes=30)
        self.now = partial(now, self)

        with self.assertRaises(Exception) as cm:
            self.interface.add_to_cart(self.valid_cart_id, object(), 1)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.EXPIRATED_CART_MSG
            )

        #ASERTAR QUE NO SE AGREGO, no se bien como hacerlo, porque si bien 
        #es que el list del carro sea el mismo, como esta expirado no podes 
        #pedir list_cart() porque esta expirado

    def test05_can_add_items_to_a_non_expirated_cart(self):
        old_items = self.interface.list_cart(self.valid_cart_id)
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)

        items_now = self.interface.list_cart(self.valid_cart_id)
        self.assertTrue(old_items != items_now )
    
    def test06_can_not_list_expirated_cart(self):
        previous_datetime = self.now()

        def now(self):
            return previous_datetime + timedelta(minutes=30)
        self.now = partial(now, self)

        with self.assertRaises(Exception) as cm:
            self.interface.list_cart(self.valid_cart_id)

        self.assertEqual(
            cm.exception.message, 
            RESTInterface.EXPIRATED_CART_MSG
            )
    
    def test07_can_list_non_expirated_cart(self):
        self.interface.list_cart(self.valid_cart_id)
        #No assertions needed?

    def test08_can_not_checkout_expirated_cart(self):
        previous_datetime = self.now()

        def now(self):
            return previous_datetime + timedelta(minutes=30)
        self.now = partial(now, self)

        with self.assertRaises(Exception) as cm:
            self.interface.checkout_cart(
                self.valid_cart_id, 
                self.credit_card_number, 
                self.card_expiration_date, 
                self.credit_card_owner
                )

        self.assertEqual(
            cm.exception.message, 
            RESTInterface.EXPIRATED_CART_MSG
            )
        # no se como asertar que no se llamo al checkout (simulador de cajero?)
        # y que el id sigue en el diccionario ?

    def test09_can_checkout_non_expirated_cart(self):
        
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        self.interface.checkout_cart(
                self.valid_cart_id, 
                self.credit_card_number, 
                self.card_expiration_date, 
                self.credit_card_owner
                )
        #Not assertion needed?       
    def test10_cart_can_only_be_checked_out_once(self):
        
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        self.interface.checkout_cart(
                self.valid_cart_id, 
                self.credit_card_number, 
                self.card_expiration_date, 
                self.credit_card_owner
                )
        with self.assertRaises(Exception) as cm:
            self.interface.checkout_cart(
                self.valid_cart_id, 
                self.credit_card_number, 
                self.card_expiration_date, 
                self.credit_card_owner
                )

        self.assertEqual(
            cm.exception.message, 
            RESTInterface.INVALID_CART_ID
            )
        #Es invalido porque tras el checkout se borra el id. 
        
    def test11_reports_invalid_credentials_trying_to_list_purchases_with_invalid_client_ID_(self):
        listed_purchases = 0
        with self.assertRaises(Exception) as cm:
            listed_purchases=self.interface.list_purchases(
                'Pedro', 
                self.juan_password
                )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )
        self.assertEqual(listed_purchases, 0)

    def test12_reports_invalid_credentials_trying_to_list_purchases_with_invalid_password(self):
        listed_purchases = 0
        with self.assertRaises(Exception) as cm:
            listed_purchases=self.interface.list_purchases(
                self.juan_id,
                'invalid_password'
                )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )
        self.assertEqual(listed_purchases, 0)

    def test13_can_create_list_purchases_with_valid_credentials(self):
        listed_purchases = 0
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        self.interface.checkout_cart(
                self.valid_cart_id, 
                self.credit_card_number, 
                self.card_expiration_date, 
                self.credit_card_owner
                )
        listed_purchases=self.interface.list_purchases(
                self.juan_id,
                self.juan_password
                )

        self.assertEqual(
            listed_purchases, 
            [((self.item_in_catalog, 1),)]
            )

    def test14_cart_ID_generator_does_never_return_the_same_ID(self):
        #hacer check out y generar otro y ver que es distinto           
        pass
    def test15_add_to_cart_reports_if_cart_ID_is_invalid(self):
        state0 = self.interface
        with self.assertRaises(Exception) as cm:
            self.interface.add_to_cart( 'invalid cart id', object(), 1)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CART_ID
            )
        self.assertEqual(state0, self.interface)


    def test16_list_cart_reports_if_cart_ID_is_invalid(self):
        state0 = self.interface
        with self.assertRaises(Exception) as cm:
            self.interface.list_cart( 'invalid cart id')

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CART_ID
            )
        self.assertEqual(state0, self.interface)    
    def test17_checkout_reports_if_cart_ID_is_invalid(self):
        state0 = self.interface
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        with self.assertRaises(Exception) as cm:
            self.interface.checkout_cart(
                    'invalid cart id', 
                    self.credit_card_number, 
                    self.card_expiration_date, 
                    self.credit_card_owner
                    )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CART_ID
            )
        self.assertEqual(state0, self.interface)

class ShoppingCart(object):

    NOT_IN_CATALOG_ERROR_MSG = "Item's not in catalog"
    QUANTITY_ERROR_MSG = "Quantity must be a positive integer"

    def __init__(self, a_catalog):
        self.items = defaultdict(int)
        self.catalog = a_catalog

    def is_empty(self):
        return len(self.items) == 0

    def add(self, item, quantity):

        if quantity <= 0:
            raise Exception(self.__class__.QUANTITY_ERROR_MSG)

        if item in self.catalog:
            self.items[item] += quantity
        else:
            raise Exception(self.__class__.NOT_IN_CATALOG_ERROR_MSG)

    def list(self): #supongo que cuando se crean las tuplas son copias. sino usar copy
        return [(item,self.number_of(item)) for item in self.items]

    def number_of(self, an_item):
        return self.items[an_item]

    def total(self):
        return sum([self.catalog.price(item)*self.number_of(item) for
                    item in self.items])

    def save_in(self, a_client_sales_book):
        a_client_sales_book.append(tuple(self.list()))

class Catalog(object):
    def __init__(self, items_with_prices):
        self._prices = items_with_prices

    def __contains__(self, an_item):
        return an_item in self._prices

    #def add(self, item, price):
    #   self._prices[item] = price

    def price(self, item):
        return self._prices[item]


class CheckoutError(Exception):
    def __init__(self, message):
        self.message = message


class CreditCard(object):
    def __init__(self, number, expiration_date, card_owner):
        # Validar parametros
        self.number = number
        self.expiration_date = expiration_date
        self.card_owner = card_owner

    def is_expirated(self, date):
        return self.expiration_date < date

    def number(self):
        return copy(self.number)
    def expiration_date(self):
        return copy(self.expiration_date)
    def owner(self):
        return copy(self.card_owner)


class MerchantProcessor(object):
    def charge(self, credit_card, amount):
        pass


class Cashier(object):
    EXPIRATED_CARD_ERROR_MSG = 'This card is no longer valid'
    EMPTY_CART_ERROR_MESSAGE = 'Can not check out an empty cart'

    def check_out(self, cart, credit_card, merchant_processor,
                  date, client_sales_book):

        if credit_card.is_expirated(date):
            raise CheckoutError(
                self.__class__.EXPIRATED_CARD_ERROR_MSG
            )
        if cart.is_empty():
            raise CheckoutError(
                self.__class__.EMPTY_CART_ERROR_MESSAGE
            )

        merchant_processor.charge(credit_card, cart.total())

        cart.save_in(client_sales_book)
        
# TODO: Creo que habría que cambiarle el nombre a esta clase
class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.item_in_catalog = object()
        self.item_not_in_catalog = object()
        self.catalog = Catalog({
            self.item_in_catalog: 10,
            "Jamon":5,
            "Queso":10
            })
        self.cart = ShoppingCart(self.catalog)

    def test01_new_cart_is_empty(self):
        self.assertTrue(self.cart.is_empty())

    def test02_may_add_copies_of_item_in_catalog_to_cart(self):
        item_to_add = self.item_in_catalog
        self.cart.add(item_to_add, 10)
        self.assertTrue(self.cart.number_of(item_to_add) >= 10)

    def test03_can_not_add_items_that_are_not_in_the_catalog(self):

        with self.assertRaises(Exception) as cm:
            self.cart.add(self.item_not_in_catalog, 1)

        self.assertEqual(
            cm.exception.message,
            ShoppingCart.NOT_IN_CATALOG_ERROR_MSG
        )

        self.assertEqual(self.cart.number_of(self.item_not_in_catalog), 0)

    def test04_can_list_items_in_cart(self):
        self.cart.add(self.item_in_catalog, 1)
        self.cart.add("Jamon", 3)
        self.cart.add("Queso", 2)
        listed_cart = [
            (self.item_in_catalog, 1),
            ('Jamon', 3),
            ('Queso', 2)
        ]

        self.assertEqual(set(listed_cart), set(self.cart.list()))


class MerchantProcessorSimulator(object):

    STOLEN_CARD_ERROR_MSG = 'Stolen card'
    UNFOUNDED_CARD_ERROR_MSG = 'Card without founds'
    CALLED_CARD_EXCEPTION_MSG = 'Called'

    def __init__(self, stolen_cards, unfounded_cards):
        self.stolen_cards = stolen_cards
        self.unfounded_cards = unfounded_cards
        self.charge_called = False

    def charge(self, credit_card, amount):
        if credit_card in self.stolen_cards:
            raise CheckoutError(self.__class__.STOLEN_CARD_ERROR_MSG)
        elif credit_card in self.unfounded_cards:
            raise CheckoutError(self.__class__.UNFOUNDED_CARD_ERROR_MSG)
        else:
            self.charge_called = True


class CashierTests(unittest.TestCase):

    def setUp(self):

        item = object()
        catalog = Catalog({item:10})
        self.merchant_processor = MerchantProcessor()
        self.client_empty_sales_book = []
        self.empty_cart = ShoppingCart(catalog)
        self.non_empty_cart = ShoppingCart(catalog)

        self.non_empty_cart.add(item, 1)

        self.cashier = Cashier()
        self.expirated_card = CreditCard(
            number=22,
            expiration_date=date.today() - timedelta(days=1),
            card_owner='Pedro de Mendoza'
        )
        self.valid_card = CreditCard(
            number=23,
            expiration_date=date.today() + timedelta(days=1),
            card_owner='Gilgamesh'
        )
        self.stolen_card = CreditCard(
            number=24,
            expiration_date=date.today() + timedelta(days=1),
            card_owner='Me'
        )
        self.unfounded_card = CreditCard(
            number=25,
            expiration_date=date.today() + timedelta(days=1),
            card_owner='You'
        )
        self.merchant_processor_simulator = MerchantProcessorSimulator(
            stolen_cards=[self.stolen_card],
            unfounded_cards=[self.unfounded_card]
        )

    def test01_can_not_checkout_empty_cart(self):

        with self.assertRaises(CheckoutError) as cm:
            self.cashier.check_out(
                cart=self.empty_cart,
                credit_card=self.valid_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client_sales_book=self.client_empty_sales_book
            )

        self.assertEqual(
            cm.exception.message,
            Cashier.EMPTY_CART_ERROR_MESSAGE,
        )
        self.assertEqual(len(self.client_empty_sales_book), 0)

    def test02_cashier_can_not_checkout_with_invalid_card(self):

        with self.assertRaises(CheckoutError) as cm:

            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.expirated_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client_sales_book=self.client_empty_sales_book
            )

        self.assertEqual(
            cm.exception.message,
            Cashier.EXPIRATED_CARD_ERROR_MSG
        )

        self.assertEqual(len(self.client_empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())
        self.assertFalse(self.merchant_processor_simulator.charge_called)

    def test03_cashier_calls_merchant_processor_if_cart_is_not_empty_and_card_is_valid(self):

        self.cashier.check_out(
            cart=self.non_empty_cart,
            credit_card=self.valid_card,
            merchant_processor=self.merchant_processor_simulator,
            date=date.today(),
            client_sales_book=self.client_empty_sales_book
        )

        self.assertTrue(self.merchant_processor_simulator.charge_called)

    def test04_can_not_sell_to_a_stolen_card(self):
        with self.assertRaises(Exception) as cm:
            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.stolen_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client_sales_book=self.client_empty_sales_book
            )

        self.assertEqual(
            MerchantProcessorSimulator.STOLEN_CARD_ERROR_MSG,
            cm.exception.message
        )
        self.assertEqual(len(self.client_empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())

    def test05_can_not_sell_to_an_unfounded_card(self):
        with self.assertRaises(Exception) as cm:
            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.unfounded_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client_sales_book=self.client_empty_sales_book
            )

        self.assertEqual(
            MerchantProcessorSimulator.UNFOUNDED_CARD_ERROR_MSG,
            cm.exception.message
        )
        self.assertEqual(len(self.client_empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())

    def test06_cashier_saves_sale_if_all_is_ok(self):
        
        self.cashier.check_out(
            cart=self.non_empty_cart,
            credit_card=self.valid_card,
            merchant_processor=self.merchant_processor_simulator,
            date=date.today(),
            client_sales_book=self.client_empty_sales_book
        )

        self.assertEqual(len(self.client_empty_sales_book), 1)
        self.assertEqual(self.client_empty_sales_book[0], tuple(self.non_empty_cart.list()) )

if __name__ == '__main__':
    unittest.main()