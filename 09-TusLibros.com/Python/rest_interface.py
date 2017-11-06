# For python this file uses encoding: utf-8
import unittest
from online_book_store import *
from collections import defaultdict, namedtuple
from datetime import date, timedelta, datetime
from copy import copy
from functools import partial
import random
import uuid

CartInformation = namedtuple('CartInformation', ['cart', 'client_ID']) 
TransactionInfo = namedtuple('TransactionInfo', ['items','catalog','total_amount'])
Sale = namedtuple('Sale', ['items','total_amount'])
 
class RESTInterface(object):

    EXPIRED_CART_MSG = 'Expirated cart'
    INVALID_CREDENTIALS = 'Invalid credentials'
    INVALID_CART_ID = 'Not existing cart ID'

    def __init__(self, users, catalog, clock, cart_ID_generator,
                 cart_validity_time, merchant_processor):
        self._users = users
        self._cart_information_by_ID = {}
        self._sales_book = {user: [] for user in users}
        self._transactionInfo = {}

        self._clock = clock
        self._catalog = catalog
        self._cart_ID_generator = cart_ID_generator
        self._cart_validity_time = cart_validity_time
        self._merchant_processor = merchant_processor
    
    def create_cart(self, client_ID, client_password):

        self.check_valid_credentials(client_ID, client_password)
        cart_ID = self._cart_ID_generator.new_ID()

        self._cart_information_by_ID[cart_ID] = CartInformation(
                    ExpirableCart(
                        ShoppingCart(self._catalog),
                        self._cart_validity_time,
                        self._clock
                        ),
                    client_ID
                    )

        return cart_ID

    def add_to_cart(self, cart_ID, book_ISBN, quantity):
        self.check_valid_cart_ID(cart_ID)
        self._cart_information_by_ID[cart_ID].cart.add(
            book_ISBN,
            quantity
        )

    def list_cart(self, cart_ID):
        self.check_valid_cart_ID(cart_ID)
        return self._cart_information_by_ID[cart_ID].cart.list()

    def checkout_cart(self, cart_ID, credit_card_number, card_expiration_date,
                      credit_card_owner):
        self.check_valid_cart_ID(cart_ID)
        
        the_cart = self._cart_information_by_ID[cart_ID].cart
        a_cashier = Cashier()
        
        a_credit_card = CreditCard(
            credit_card_number,
            card_expiration_date,
            credit_card_owner
        )
        
        client_ID = self._cart_information_by_ID[cart_ID].client_ID
        
        transaction_ID, total_amount = a_cashier.check_out(
            cart=the_cart,
            credit_card=a_credit_card,
            merchant_processor= self._merchant_processor,
            date=self._clock.now().date(),
            client_sales_book = self._sales_book[client_ID]
            )

        self._transactionInfo[transaction_ID] = TransactionInfo(
            the_cart.list(), 
            the_cart.catalog(), 
            total_amount
            )

        # Decision de implementacion, la venta la guarda el cashier
        self._cart_information_by_ID.pop(cart_ID)
        return transaction_ID, total_amount

    def list_purchases(self, client_ID, client_password):
        self.check_valid_credentials(client_ID, client_password)
        
        listed_purchases = {} 
        total_amount = 0  
        for sale in self._sales_book[client_ID]:
            total_amount += sale.total_amount
            for isbn, quantity in sale.items:
                if isbn not in listed_purchases:
                    listed_purchases[isbn] = quantity
                else:
                    listed_purchases[isbn]+= quantity 

        return listed_purchases, total_amount

#auxiliares privadas
 
    def check_valid_credentials(self, user, password):
        if (user not in self._users) or password != self._users[user]:
            raise Exception(self.__class__.INVALID_CREDENTIALS)

    def check_valid_cart_ID(self, cart_ID):
        if cart_ID not in self._cart_information_by_ID.keys():
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
    def new_ID(self):
        return uuid.uuid4()


class RESTTests(unittest.TestCase):

    def setUp(self):
        self.juan_id = 'Juan'
        self.juan_password = 'password'
        self.users = {
            self.juan_id: self.juan_password
        }
        self.item_in_catalog = object()
        self.catalog = Catalog({self.item_in_catalog: 10})
        self.validity_time = timedelta(minutes=30)
        self.interface = RESTInterface(
            self.users,
            self.catalog,
            self,
            CartIDGenerator(),
            self.validity_time,
            MerchantProcessorSimulator([],[])
        )
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

    def fast_forward(self, amount):
        previous_datetime = self.now()

        def now(self):
            return previous_datetime + amount
        self.now = partial(now, self)

    def test01_can_not_create_cart_with_invalid_username(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart('Pedro', self.juan_password)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )

    def test02_can_not_create_cart_with_invalid_password(self):
        with self.assertRaises(Exception) as cm:
            self.interface.create_cart(self.juan_id, 'invalid_password')

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )

    def test03_cart_created_with_valid_credentials_is_empty(self):
        self.assertEqual(len(self.interface.list_cart(self.valid_cart_id)), 0)

    def test04_can_not_add_items_to_an_expired_cart(self):
        self.fast_forward(self.validity_time)

        with self.assertRaises(Exception) as cm:
            self.interface.add_to_cart(self.valid_cart_id, object(), 1)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.EXPIRED_CART_MSG
        )

    def test05_can_add_items_to_a_non_expired_cart(self):
        old_items = self.interface.list_cart(self.valid_cart_id)
        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)

        items_now = self.interface.list_cart(self.valid_cart_id)

        self.assertTrue(old_items != items_now)
        # supongo que verificar que cambio alcanza, verificar que agrega bien
        # creo yo es responsabilidad de un test unitario del carro.

    def test06_can_not_list_expired_cart(self):
        self.fast_forward(self.validity_time)

        with self.assertRaises(Exception) as cm:
            self.interface.list_cart(self.valid_cart_id)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.EXPIRED_CART_MSG
        )

    def test08_can_not_checkout_expired_cart(self):
        self.fast_forward(self.validity_time)

        with self.assertRaises(Exception) as cm:
            self.interface.checkout_cart(
                self.valid_cart_id,
                self.credit_card_number,
                self.card_expiration_date,
                self.credit_card_owner
            )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.EXPIRED_CART_MSG
        )
        self.assertEqual(
            len(self.interface.list_purchases(self.juan_id, self.juan_password)[0]
                ),
            0
            )

    def test09_can_checkout_non_expired_cart(self):

        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        self.interface.checkout_cart(
                self.valid_cart_id,
                self.credit_card_number,
                self.card_expiration_date,
                self.credit_card_owner
                )

        self.assertEqual(self.interface.list_purchases(
            self.juan_id,
            self.juan_password
            ),
            ({self.item_in_catalog: 1} , 10)
        )

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

    def test11_reports_invalid_credentials_trying_to_list_purchases_with_invalid_client_ID_(self):

        with self.assertRaises(Exception) as cm:
                self.interface.list_purchases(
                    'Pedro',
                    self.juan_password
                )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )

    def test12_reports_invalid_credentials_trying_to_list_purchases_with_invalid_password(self):

        with self.assertRaises(Exception) as cm:
                self.interface.list_purchases(
                    self.juan_id,
                    'invalid_password'
                )

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CREDENTIALS
        )

    def test13_can_create_list_purchases_with_valid_credentials(self):

        self.interface.add_to_cart(self.valid_cart_id, self.item_in_catalog, 1)
        self.interface.checkout_cart(
                self.valid_cart_id,
                self.credit_card_number,
                self.card_expiration_date,
                self.credit_card_owner
                )
        listed_purchases = self.interface.list_purchases(
                self.juan_id,
                self.juan_password
            )


        self.assertEqual(listed_purchases[0],{self.item_in_catalog:1})
        self.assertEqual(listed_purchases[1],10)

    def test14_cart_ID_generator_does_never_return_the_same_ID(self):
        cart_id = self.interface.create_cart(self.juan_id, self.juan_password)
        self.assertNotEqual(cart_id, self.valid_cart_id)

    def test15_add_to_cart_reports_if_cart_ID_is_invalid(self):
        with self.assertRaises(Exception) as cm:
            self.interface.add_to_cart('invalid cart id', object(), 1)

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CART_ID
        )

    def test16_list_cart_reports_if_cart_ID_is_invalid(self):
        state0 = self.interface
        with self.assertRaises(Exception) as cm:
            self.interface.list_cart('invalid cart id')

        self.assertEqual(
            cm.exception.message,
            RESTInterface.INVALID_CART_ID
            )

    def test17_checkout_reports_if_cart_ID_is_invalid(self):
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

if __name__ == '__main__':
    unittest.main()
