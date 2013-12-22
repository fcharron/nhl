#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import datetime

from nhl import datatypes



class TestDatatypes(unittest.TestCase):

    def test_minutes(self):
      self.assertEqual(datetime.timedelta(seconds=0), 
                    datatypes.minutes_as_time("0"))


    def test_minutes2(self):
      self.assertEqual(datetime.timedelta(seconds=10,minutes=200), 
                    datatypes.minutes_as_time("200:10"))


    def test_minutes3(self):
      self.assertEqual(datetime.timedelta(seconds=10,minutes=7000), 
                    datatypes.minutes_as_time("7,000:10"))

    def test_season(self):
      self.assertEqual("20122013", datatypes.season("2012-2013"))



if __name__ == '__main__': 
    unittest.main()