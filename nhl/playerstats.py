#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''playerstats.py

Example usage:

    q = Query()
    q.season("20132014").playoffs().position("S").summary()

    for n, p in enumerate(q):
        print n, p

'''

from urllib import urlencode
from urllib2 import urlparse
import re

from commons import getdoc
from commons import stringify


PLAYERSTATS_URL = "http://www.nhl.com/ice/playerstats.htm"


def get_nhlid_from_tablerow(tr):
    '''Get player ID from href inside the row'''
    anchor_tag = tr.find(".//a[@href]")
    if anchor_tag is not None:
        href = anchor_tag.attrib['href']
    if re.match(r"^/ice/player.htm", href):
        qs = urlparse.urlparse(href).query
        return urlparse.parse_qs(qs).get("id", None)[0]


def get_table_columns(table):
    '''Returns the column names for the table.
    We skips first col, as it's only the row number.
    We add NHL ID and Number columns in the beginnnig.
    '''
    thead = table.find("thead")
    columns = [stringify(th) for th in thead.findall(".//th")]
    return ['nhl_id', 'number'] + columns[1:]


def get_table_pages_urls(url):
    '''Gets URLS for pages of the table at the given URL'''

    doc = getdoc(url)

    urls = []
    pages_div = doc.find(".//div[@class='pages']")

    #Check for empty table
    if pages_div is None:
        return urls

    #Check for one page table
    page_anchors = pages_div.findall("a")
    if len(page_anchors) < 1:
        urls.append(url)  # One page table
        return urls

    #Get the last page anchor
    last_anchor = page_anchors[-1]
    last_anchor_href = last_anchor.get("href")

    #Get the number of the last page
    pattern = re.compile(r"(\d+)")
    number_of_pages = pattern.findall(last_anchor_href)[-1]

    #Load all pages
    NHL_BASE_URL = "http://www.nhl.com"
    for p in range(1, int(number_of_pages) + 1):
        page_url = last_anchor_href.replace("pg=" + number_of_pages,
                                            "pg=" + str(p))
        urls.append(NHL_BASE_URL + page_url)

    return urls


def readrows(urls, limit=None):
    '''Reads all or a limited numbers of rows from the table'''

    row_counter = 0
    for url in urls:

        doc = getdoc(url)

        table = doc.find(".//table[@class='data stats']")

        if row_counter == 0:
            yield get_table_columns(table)

        tbody = table.find("tbody")

        if tbody is None:
            raise StopIteration

        for tr in tbody.findall('tr'):

            if limit is not None and row_counter == limit:
                raise StopIteration

            nhl_id = get_nhlid_from_tablerow(tr)

            data = [nhl_id] + [stringify(td) for td in tr.findall("td")]

            yield data

            row_counter += 1


class Query:
    '''Query for playerstats'''

    def __str__(self):
        return self.url()

    def season(self, s):
        if re.match(r"\d{8}", s):
            self.season = s
        return self

    def regular(self):
        self.gameType = 2
        return self

    def playoffs(self):
        self.gameType = 3
        return self

    def team(self, t):
        if re.match(r"[A-Z]{3}", t):
            self.team = t
        return self

    def country(self, c):
        if re.match(r"[A-Z]{3}", c):
            self.country = c
        return self

    def position(self, p):
        if p in ("S", "C", "D", "F", "G", "L", "R"):
            self.position = p
        return self

    def summary(self):
        self.viewName = 'summary'
        return self

    def bios(self):
        self.viewName = 'bios'
        return self

    def url(self):
        '''Builds the URL based on parameters'''
        if self.position == 'G' and self.viewName == 'bios':
            self.viewName = 'goalieBios'

        query = self.__dict__

        url = PLAYERSTATS_URL + "?" + urlencode(query)

        return url

    def run(self, limit=None):
        urls = get_table_pages_urls(self.url())
        return readrows(urls, limit)

    def fetch(self, limit=None):
        result = []
        for p in self.run(limit):
            result.append(p)
        return result

    def __iter__(self):
        return self.run()


if __name__ == '__main__':
    q = Query()

    q.season("20132014").playoffs().position("G").bios()

    for row in q.run():
        print row
