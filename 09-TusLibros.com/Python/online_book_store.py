# For python this file uses encoding: utf-8
import unittest
from online_book_store import *
from collections import defaultdict, namedtuple
from datetime import date, timedelta, datetime
from copy import copy
from functools import partial
import random
import uuid

Sale = namedtuple('Sale', ['items','total_amount'])
 
class ShoppingCart(object):

    NOT_IN_CATALOG_ERROR_MSG = "Item's not in catalog"
    QUANTITY_ERROR_MSG = "Quantity must be a positive integer"

    def __init__(self, a_catalog):
        self.items = defaultdict(int)
        self._catalog = a_catalog

    def is_empty(self):
        return len(self.items) == 0

    def add(self, item, quantity):

        if quantity <= 0:
            raise Exception(self.__class__.QUANTITY_ERROR_MSG)

        if item in self._catalog:
            self.items[item] += quantity
        else:
            raise Exception(self.__class__.NOT_IN_CATALOG_ERROR_MSG)

    def list(self):
        # supongo que cuando se crean las tuplas son copias. sino usar copy
        return [(item, self.number_of(item)) for item in self.items]
    
    def catalog(self):
        return self._catalog

    def number_of(self, an_item):
        return self.items[an_item]

    def total(self):
        return round(sum([self._catalog.price(item)*self.number_of(item) for
                    item in self.items]), 2)

class Catalog(object):
    def __init__(self, items_with_prices):
        self._prices = items_with_prices

    def __contains__(self, an_item):
        return an_item in self._prices

    # def add(self, item, price):
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

    def is_expired(self, date):
        return self.expiration_date < date

    def number(self):
        return copy(self.number)

    def expiration_date(self):
        return copy(self.expiration_date)

    def owner(self):
        return copy(self.card_owner)


class Cashier(object):
    EXPIRATED_CARD_ERROR_MSG = 'This card is no longer valid'
    EMPTY_CART_ERROR_MESSAGE = 'Can not check out an empty cart'

    def check_out(self, cart, credit_card, merchant_processor,
                  date, client_sales_book):

        if credit_card.is_expired(date):
            raise CheckoutError(
                self.__class__.EXPIRATED_CARD_ERROR_MSG
            )
        if cart.is_empty():
            raise CheckoutError(
                self.__class__.EMPTY_CART_ERROR_MESSAGE
            )

        transaction_amount = cart.total()
        transaction_ID = merchant_processor.charge(credit_card,transaction_amount)
        sale = Sale(cart.list(),transaction_amount)
        client_sales_book.append(sale)

        return transaction_ID,transaction_amount

class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.item_in_catalog = object()
        self.item_not_in_catalog = object()
        self.catalog = Catalog({
            self.item_in_catalog: 10,
            "Jamon": 5,
            "Queso": 10
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


class MerchantProcessor(object):
    #Clase de produccion
    def charge(self, credit_card, amount):
        pass


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
            transaction_ID = uuid.uuid4()
            self.charge_called = True
            return transaction_ID

class CashierTests(unittest.TestCase):

    def setUp(self):

        item = object()
        catalog = Catalog({item: 10})
        self.merchant_processor = MerchantProcessor()
        self.client_empty_sales_book = []
        self.empty_cart = ShoppingCart(catalog)
        self.non_empty_cart = ShoppingCart(catalog)

        self.non_empty_cart.add(item, 1)

        self.cashier = Cashier()
        self.expired_card = CreditCard(
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
        self.assertFalse(self.merchant_processor_simulator.charge_called)
        self.assertEqual(len(self.client_empty_sales_book),0)

    def test02_cashier_can_not_checkout_with_invalid_card(self):

        with self.assertRaises(CheckoutError) as cm:

            self.cashier.check_out(
                cart=self.non_empty_cart,
                credit_card=self.expired_card,
                merchant_processor=self.merchant_processor_simulator,
                date=date.today(),
                client_sales_book=self.client_empty_sales_book
            )

        self.assertEqual(
            cm.exception.message,
            Cashier.EXPIRATED_CARD_ERROR_MSG
        )

        self.assertFalse(self.non_empty_cart.is_empty())
        self.assertFalse(self.merchant_processor_simulator.charge_called)
        self.assertEqual(len(self.client_empty_sales_book),0)

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
        self.assertFalse(self.non_empty_cart.is_empty())
        self.assertEqual(len(self.client_empty_sales_book),0)

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
        self.assertFalse(self.non_empty_cart.is_empty())
        self.assertEqual(len(self.client_empty_sales_book),0)

    def test06_cashier_saves_sale_if_everything_is_ok(self):

        self.cashier.check_out(
            cart=self.non_empty_cart,
            credit_card=self.valid_card,
            merchant_processor=self.merchant_processor_simulator,
            date=date.today(),
            client_sales_book=self.client_empty_sales_book
        )

        self.assertEqual(len(self.client_empty_sales_book), 1)
        self.assertEqual(
            self.client_empty_sales_book[0].items,
            self.non_empty_cart.list()
        )
        self.assertEqual(
            self.client_empty_sales_book[0].total_amount,
            self.non_empty_cart.total()
        )
    

if __name__ == '__main__':
    unittest.main()
