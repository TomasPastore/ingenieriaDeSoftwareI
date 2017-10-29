# For python this file uses encoding: utf-8
import unittest
from collections import defaultdict


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
        self._items = set()

    def __contains__(self, an_item):
        return an_item in self._items

    def add_item(self, item):
        self._items.add(item)


class Cashier(object):
    pass


# TODO: Creo que habría que cambiarle el nombre a esta clase
class ShoppingCartTest(unittest.TestCase):

    def setUp(self):
        self.item_in_catalog = object()
        self.item_not_in_catalog = object()
        catalog = Catalog()
        catalog.add_item(self.item_in_catalog)
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

    def test01_xxx(self):
        pass


if __name__ == '__main__':
    unittest.main()
