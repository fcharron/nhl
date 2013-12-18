#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bs4 import BeautifulSoup

from nhl import scraper


class TestNhl(unittest.TestCase):

    def test_get_qp(self):
        row = BeautifulSoup('<tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1" style="text-align: left;"><a href="/ice/player.htm?id=8471675">Sidney Crosby</a></td><td colspan="1" rowspan="1" style="text-align: center;"><a style="border-bottom:1px dotted;" onclick="loadTeamSpotlight(jQuery(this));" rel="PIT" href="javascript:void(0);">PIT</a></td><td colspan="1" rowspan="1" style="text-align: center;">C</td><td colspan="1" rowspan="1" style="center">35</td><td colspan="1" rowspan="1" style="center">19</td><td colspan="1" rowspan="1" style="center">28</td><td colspan="1" rowspan="1" style="center" class="active">47</td><td colspan="1" rowspan="1" style="center">+4</td><td colspan="1" rowspan="1" style="center">20</td><td colspan="1" rowspan="1" style="center">6</td><td colspan="1" rowspan="1" style="center">0</td><td colspan="1" rowspan="1" style="center">4</td><td colspan="1" rowspan="1" style="center">1</td><td colspan="1" rowspan="1" style="center">117</td><td colspan="1" rowspan="1" style="center">16.2</td><td colspan="1" rowspan="1" style="center">22:14</td><td colspan="1" rowspan="1" style="center">23.9</td><td colspan="1" rowspan="1" style="center">51.2</td></tr>')

        nhl_id = int(scraper.get_qp_from_href(row, "id", "/ice/player.htm"))
        self.assertEqual(nhl_id, 8471675)


if __name__ == '__main__': 
    unittest.main()


