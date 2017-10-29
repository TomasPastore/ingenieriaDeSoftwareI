# For python this file uses encoding: utf-8
import unittest
from collections import defaultdict
from datetime import date, timedelta


class ShoppingCart(object):

    NOT_IN_CATALOG_ERROR_MSG = "Item's not in catalog"

    def __init__(self, a_catalog):
        self.items = defaultdict(int)
        self.catalog = a_catalog

    def is_empty(self):
        return len(self.items) == 0

    def add(self, item, quantity):
        if item in self.catalog:
            self.items[item] += quantity
        else:
            raise Exception(self.__class__.NOT_IN_CATALOG_ERROR_MSG)

    def number_of(self, an_item):
        return self.items[an_item]


class Catalog(object):
    def __init__(self, *args, **kwargs):
        # Esto no es inmutable, así que yo le pasaría items iniciales...
        self._items = set()

    def __contains__(self, an_item):
        return an_item in self._items

    def add(self, item):
        self._items.add(item)


class CheckoutError(Exception):
    def __init__(self, message):
        self.message = message


class CreditCard(object):
    def __init__(self, number, expiration_date, card_owner):
        self.number = number
        self.expiration_date = expiration_date
        self.card_owner = card_owner


class Cashier(object):
    EXPIRATED_CARD_ERROR_MSG = 'This card is no longer valid'
    EMPTY_CART_ERROR_MESSAGE = 'Can not check out an empty cart'

    def check_out(self, cart, credit_card):
        # < o <=????
        if credit_card.expiration_date < date.today():
            raise CheckoutError(
                self.__class__.EXPIRATED_CARD_ERROR_MSG
                )
        if cart.is_empty:
            raise CheckoutError(
                self.__class__.EMPTY_CART_ERROR_MESSAGE
            )


# TODO: Creo que habría que cambiarle el nombre a esta clase
class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.item_in_catalog = object()
        self.item_not_in_catalog = object()
        catalog = Catalog()
        catalog.add(self.item_in_catalog)
        self.cart = ShoppingCart(catalog)

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

        # No estoy seguro de si esta es la mejor manera de chequearlo...
        # O más bien, no estoy seguro de que esto no tenga que
        # tirar una excepción

        self.assertEqual(self.cart.number_of(self.item_not_in_catalog), 0)


class CashierTests(unittest.TestCase):

    def setUp(self):
        catalog = Catalog()
        item = object()
        catalog.add(item)
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

    def test01_can_not_checkout_empty_cart(self):
        with self.assertRaises(CheckoutError) as cm:
            self.cashier.check_out(self.empty_cart, self.valid_card)

        self.assertEqual(
            cm.exception.message,
            Cashier.EMPTY_CART_ERROR_MESSAGE,
        )

    def test02_cashier_can_not_checkout_with_invalid_card(self):
        with self.assertRaises(CheckoutError) as cm:
            self.cashier.check_out(self.non_empty_cart, self.expirated_card)

        self.assertEqual(
            cm.exception.message,
            Cashier.EXPIRATED_CARD_ERROR_MSG
        )

        self.assertFalse(self.non_empty_cart.is_empty())


if __name__ == '__main__':
    unittest.main()
