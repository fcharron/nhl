#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from lxml import etree

PAGES = {}


class NHlException(Exception):
    pass


def getdoc(url):
    '''Returns the HTML DOM as an etree Elementree'''
    if url not in PAGES:
        try:
            response = urlopen(url)
            content = response.read().decode('utf-8')
            parser = etree.HTMLParser()
        except Exception as e:
            raise SystemExit(e.message)

        PAGES[url] = etree.fromstring(content, parser)

    return PAGES[url]


def stringify(element):
    '''Concatenates all text in the subelements into one string'''
    return u"".join([x for x in element.itertext()]).strip().replace("\n",
                                                                     " ")
