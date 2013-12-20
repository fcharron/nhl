#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

import nhl



ROWS_TO_GET = 7

class TestNhl(unittest.TestCase):

   	def test0(self):
   		forsberg = nhl.player(8458520)
   		self.assertTrue(len(forsberg.career().fetch(ROWS_TO_GET)), ROWS_TO_GET)

  	def test1(self):
  		crawford = nhl.player(8470645)
   		self.assertTrue(len(crawford.career().fetch(ROWS_TO_GET)), ROWS_TO_GET)


	def test2(self):
		kessel = nhl.player(8473548)
		self.assertEqual(kessel.twitter(), "PKessel81")



if __name__ == '__main__': 
    unittest.main()