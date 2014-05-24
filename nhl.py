#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from urllib import urlencode
from urllib2 import urlparse
from lxml import etree
import re


__author__ = "Peter N Stark"
__version__ = "3.0"

NHL_BASE_URL = "http://www.nhl.com/ice/playerstats.htm"


class NhlPlayerStatsException(Exception):
    pass


PAGES = {}


def getdoc(url):
    '''Returns the HTML DOM as an etree Elementree'''
    if url not in PAGES:
        response = urlopen(url)
        content = response.read().decode('utf-8')
        parser = etree.HTMLParser()
        PAGES[url] = etree.fromstring(content, parser)
    return PAGES[url]


def stringify(element):
    '''Concatenates all text in the subelements into one string'''
    return u"".join([x for x in element.itertext()])


def get_nhlid_from_tablerow(tr):
    #Get player ID from href inside the row
    anchor_tag = tr.find(".//a[@href]")
    if anchor_tag is not None:
        href = anchor_tag.attrib['href']
    if re.match(r"^/ice/player.htm", href):
        qs = urlparse.urlparse(href).query
        return urlparse.parse_qs(qs).get("id", None)[0]


def cleanup_columnname(name):
    clean_name = name.strip().lower().replace("+/-", "plusminus").replace("%", "perc").replace("/", "").replace("#", "number").replace(" ", "")
    return clean_name


def get_table_columns(table):
    thead = table.find("thead")
    columns = map(cleanup_columnname,
                  [stringify(th) for th in thead.findall(".//th")])
    return ['nhl_id', 'number'] + columns[1:]


def get_page_urls(url):

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

    #Create rowdata class from table columns
    #rowdataclass = namedtuple("PlayerStats", self.table.columns)

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
    def __init__(self):
        self.q = {
            'season': "20132014",
            'gameType': 2,  # regular
            'team': "",
            'country': "",
            'position': "S"  # all skaters
        }

    def __str__(self):
        return self.url()

    def season(self, s):
        if re.match(r"\d{8}", s):
            self.q['season'] = s
        return self

    def regular(self):
        self.q['gameType'] = 2
        return self

    def playoffs(self):
        self.q['gameType'] = 3
        return self

    def team(self, t):
        if re.match(r"[A-Z]{3}", t):
            self.q['team'] = t
        return self

    def country(self, c):
        if re.match(r"[A-Z]{3}", c):
            self.q['country'] = c
        return self

    def position(self, p):
        if p in ("C", "D", "F", "G", "L", "R"):
            self.q['position'] = p
        return self

    def summary(self):
        self.q['viewName'] = 'summary'
        return self

    def bios(self):
        self.q['viewName'] = 'bios'
        return self

    def url(self):
        '''Builds the URL based on parameters'''
        if self.q['position'] == 'G' and self.q['viewName'] == 'bios':
            self.q['viewName'] = 'goalieBios'

        url = NHL_BASE_URL + "?" + urlencode(self.q)

        return url

    def run(self, limit=None):
        urls = get_page_urls(q.url())
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

    for n, p in enumerate(q):
        print n, p
