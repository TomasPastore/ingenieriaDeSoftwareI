#For python this file uses encoding: utf-8
import unittest
from collections import defaultdict

class ShoppingCart(object):
	
	def __init__(self,*args,**kwargs):
		self.copies_by_title = defaultdict(int)

	def is_empty(self):
		return len(self.copies_by_title) == 0

	def add_title(self,a_title,copies):
		self.copies_by_title[a_title] += copies 
	
	def content(self):
		return self.copies_by_title

class Catalog(object):
	pass

class ShoppingCartTest(unittest.TestCase):
	
	def setUp(self):
		self.cart = ShoppingCart()

	def test01_new_cart_is_empty(self):
		self.assertTrue(self.cart.is_empty())

	def test02_may_add_title_copies_to_cart(self):
		a_title = object()
		self.cart.add_title(a_title,10)
		self.assertTrue( self.cart.content()[a_title] >= 10 )

	def test03_xxx(self):
		pass

if __name__ == '__main__':
	unittest.main()