# For python this file uses encoding: utf-8
import unittest
from collections import defaultdict
from datetime import date, timedelta
from copy import copy

class RESTInterface(object):

    INVALID_CREDENTIALS = 'Invalid credentials'

    def __init__(self, users):
        self._cart_information_by_ID = {}
        self._sales_books = {}
        self._users = users

    def create_cart(self, client_ID, client_password):
        cart_ID = object()

        if client_ID in self._users:
            if client_password == self._users[client_ID]:
                return cart_ID
            else:
                raise Exception(self.__class__.INVALID_CREDENTIALS)
        else:
            raise Exception(self.__class__.INVALID_CREDENTIALS) 


    def add_to_cart(self, cart_ID, book_ISBN, quantity):
        pass

    def list_cart(self, cart_ID):
        return cart.list()
        
    def checkout_cart(self, cart_ID, credit_card_number, card_expiration_date, credit_card_owner):
        pass

    def list_purchases(self, client_ID, client_password):
        return self._sales_books[client]

class RESTTests(unittest.TestCase):
    
    def setUp(self):
        self.juan_password = 'password'
        self.users = {
            'Juan':self.juan_password
        }
        self.interface = RESTInterface(self.users)


    def test01_can_not_create_cart_with_invalid_username(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart('Pedro', self.juan_password)

        self.assertEqual(cm.exception.message, RESTInterface.INVALID_CREDENTIALS)

    def test02_can_not_create_cart_with_invalid_password(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart('Juan', 'invalid_password')

        self.assertEqual(cm.exception.message, RESTInterface.INVALID_CREDENTIALS)



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

    def list(self):
        return copy(dict(self.items))

    def number_of(self, an_item):
        return self.items[an_item]

    def total(self):
        return sum([self.catalog.price(item)*self.number_of(item) for
                    item in self.list()])


class Catalog(object):
    def __init__(self, *args, **kwargs):
        # Esto no es inmutable, así que yo le pasaría items iniciales...
        self._prices = {}

    def __contains__(self, an_item):
        return an_item in self._prices

    def add(self, item, price):
        self._prices[item] = price

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


class MerchantProcessor(object):
    def charge(self, credit_card, amount):
        pass


class Cashier(object):
    EXPIRATED_CARD_ERROR_MSG = 'This card is no longer valid'
    EMPTY_CART_ERROR_MESSAGE = 'Can not check out an empty cart'

    def check_out(self, cart, credit_card, merchant_processor,
                  date, client, sales_book):

        if credit_card.is_expirated(date):
            raise CheckoutError(
                self.__class__.EXPIRATED_CARD_ERROR_MSG
            )
        if cart.is_empty():
            raise CheckoutError(
                self.__class__.EMPTY_CART_ERROR_MESSAGE
            )

        merchant_processor.charge(credit_card, cart.total())

        sales_book[client] = copy(cart)


# TODO: Creo que habría que cambiarle el nombre a esta clase
class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.item_in_catalog = object()
        self.item_not_in_catalog = object()
        self.catalog = Catalog()
        self.catalog.add(self.item_in_catalog, 10)
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
        self.catalog.add("Jamon", 5)
        self.catalog.add("Queso", 10)
        self.cart.add(self.item_in_catalog, 1)
        self.cart.add("Jamon", 3)
        self.cart.add("Queso", 2)
        dictionary = {
            self.item_in_catalog: 1,
            'Jamon': 3,
            'Queso': 2,
        }
        self.assertEqual(dictionary, self.cart.list())

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

        catalog = Catalog()
        item = object()
        catalog.add(item, 10)
        self.merchant_processor = MerchantProcessor()
        self.client = object()
        self.empty_sales_book = {}
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
                client=self.client,
                sales_book=self.empty_sales_book
            )

        self.assertEqual(
            cm.exception.message,
            Cashier.EMPTY_CART_ERROR_MESSAGE,
        )
        self.assertEqual(len(self.empty_sales_book), 0)

    def test02_cashier_can_not_checkout_with_invalid_card(self):

        with self.assertRaises(CheckoutError) as cm:

            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.expirated_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client=self.client,
                sales_book=self.empty_sales_book
            )

        self.assertEqual(
            cm.exception.message,
            Cashier.EXPIRATED_CARD_ERROR_MSG
        )

        self.assertEqual(len(self.empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())
        self.assertFalse(self.merchant_processor_simulator.charge_called)

    def test03_can_checkout_non_empty_cart(self):

        self.cashier.check_out(
            cart=self.non_empty_cart,
            credit_card=self.valid_card,
            merchant_processor=self.merchant_processor_simulator,
            date=date.today(),
            client=self.client,
            sales_book=self.empty_sales_book
        )

        self.assertEqual(len(self.empty_sales_book), 1)
        self.assertTrue(self.merchant_processor_simulator.charge_called)

    def test04_can_not_sell_to_a_stolen_card(self):
        with self.assertRaises(Exception) as cm:
            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.stolen_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client=self.client,
                sales_book=self.empty_sales_book
            )

        self.assertEqual(
            MerchantProcessorSimulator.STOLEN_CARD_ERROR_MSG,
            cm.exception.message
        )
        self.assertEqual(len(self.empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())

    def test05_can_not_sell_to_an_unfounded_card(self):
        with self.assertRaises(Exception) as cm:
            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.unfounded_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client=self.client,
                sales_book=self.empty_sales_book
            )

        self.assertEqual(
            MerchantProcessorSimulator.UNFOUNDED_CARD_ERROR_MSG,
            cm.exception.message
        )
        self.assertEqual(len(self.empty_sales_book), 0)
        self.assertFalse(self.non_empty_cart.is_empty())

# Robada, sin credito, ver que no hable con el merchant si salto excepcion


if __name__ == '__main__':
    unittest.main()
