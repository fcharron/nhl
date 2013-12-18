#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''scraper.py

Utility functions for reading tables. 

'''

from bs4 import BeautifulSoup
import urllib2
import re
import logging
import urlparse

NHL_BASE_URL = "http://www.nhl.com"


def get_soup(url):
    '''Returns a BeautifulSoup object from the given URL'''

    try: 
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        logging('Could not load {}, {}'.format(url, e.message))
        raise e

    return soup  


def get_qp_from_href(row, name, href_string):
    '''Returns a query parameter value from the href value

    Example:
    With href_string = '/ice/player.htm?id=8471675'

    The function returns 8471675

    '''
    p = "^" + href_string
    anchor_tag = row.find(href=re.compile(p))  

    if anchor_tag:
        href = anchor_tag.attrs['href']
        query = urlparse.parse_qs(urlparse.urlparse(href).query)    
        param = query.get(name, None)
        if param:
            return param[0]  


def get_urls_for_paginated_table(url):
    '''Returns list of URLs for paginated tables at:
    http://www.nhl.com/ice/playerstats.htm
    ''' 

    #Load the first page
    soup = get_soup(url)

    #Get all anchors with page links
    pages = soup.find('div', 'pages')
    all_anchors = pages.find_all("a")
    number_of_anchors = len(all_anchors)
    
    #Get the last page anchor
    last_anchor = all_anchors[number_of_anchors-1]
    last_anchor_href = last_anchor.get("href")
    
    #Get the number of the last page
    pattern = re.compile(r"(\d+)")
    number_of_pages =  pattern.findall(last_anchor_href)[-1]

    #Load all pages
    urls = []
    for p in range(1,int(number_of_pages)+1):
        page_url = NHL_BASE_URL + last_anchor_href.replace("pg="+number_of_pages,"pg="+str(p) )
        urls.append(page_url)

    return urls          

