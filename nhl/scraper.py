#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''scraper.py

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
    '''Returns a query parameter value from the href value'''

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


if __name__ == '__main__':

    url = "http://www.nhl.com/ice/playerstats.htm?season=20132014&gameType=2&team=&position=S&country=&status=&viewName=summary"

    print get_urls_for_paginated_table(url)


    row = BeautifulSoup("""<tr><td colspan="1" rowspan="1">1</td><td colspan="1" rowspan="1" style="text-align: left;"><a href="/ice/player.htm?id=8471675">Sidney Crosby</a></td><td colspan="1" rowspan="1" style="text-align: center;"><a style="border-bottom:1px dotted;" onclick="loadTeamSpotlight(jQuery(this));" rel="PIT" href="javascript:void(0);">PIT</a></td><td colspan="1" rowspan="1" style="text-align: center;">C</td><td colspan="1" rowspan="1" style="center">35</td><td colspan="1" rowspan="1" style="center">19</td><td colspan="1" rowspan="1" style="center">28</td><td colspan="1" rowspan="1" style="center" class="active">47</td><td colspan="1" rowspan="1" style="center">+4</td><td colspan="1" rowspan="1" style="center">20</td><td colspan="1" rowspan="1" style="center">6</td><td colspan="1" rowspan="1" style="center">0</td><td colspan="1" rowspan="1" style="center">4</td><td colspan="1" rowspan="1" style="center">1</td><td colspan="1" rowspan="1" style="center">117</td><td colspan="1" rowspan="1" style="center">16.2</td><td colspan="1" rowspan="1" style="center">22:14</td><td colspan="1" rowspan="1" style="center">23.9</td><td colspan="1" rowspan="1" style="center">51.2</td></tr>""")


    print get_qp_from_href(row, "id", "/ice/player.htm")