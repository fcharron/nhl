#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''reader.py

A module for reading stats from nhl.com
'''

from bs4 import BeautifulSoup
import urllib2
import re
import logging

NHL_BASE_URL = "http://www.nhl.com"


PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={season}&gameType={gametype}&team=&position={position}&country=&status=&viewName={viewname}'



class NhlException(Exception):
    pass


def get_soup(url):
    '''Returns a BeautifulSoup object from the given URL'''

    try: 
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        logging('Could not load {}, {}'.format(url, e.message))
        raise NhlException(e.message)

    return soup



class StatsReader(object):
    '''Abstract class for reading a paginated table of stats from nhl.com. Different kinds of tables are implemented by sub classes'''

    number_of_rows = 0    
    fieldnames = ()

    def _readrow(self, stats_table):
        '''Yields one row from the table as a list'''
        for tr in stats_table.find('tbody').findAll('tr'):
            
            tds = tr.findAll('td')
            
            row = {}        
            for d in range(len(self.fieldnames)):
                val = tds[d].string
                if val:
                    row[self.fieldnames[d]] = val.encode('utf-8')
                else:
                    row[self.fieldnames[d]] = None
            yield row


    def _get_all_pages(self):
        '''Yields URLs for player stats pages''' 

        #Load the first page
        soup = get_soup(self._url)

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
        for p in range(1,int(number_of_pages)+1):
            page_url = NHL_BASE_URL + last_anchor_href.replace("pg="+number_of_pages,"pg="+str(p) )
            yield page_url
            


    def __iter__(self):
        '''Yields rows from the paginated table'''

        for page in self._get_all_pages():
            try: 
                soup = get_soup (page)
                stats_table = soup.find('table', 'stats')
            except:
                logging.warning("Could not read {}".format(page))
                raise StopIteration
            
            for row in self._readrow(stats_table):
                self.number_of_rows += 1
                yield row



GAMETYPE_MAP = {
    'regular' : 2,
    'playoff' : 3
}


class BiosReader(StatsReader):
    '''Reads the Bios Report table from nhl.com''' 
    fieldnames = ('Number','Player','Team','Pos','DOB','BirthCity','S_P', 'Ctry', 'HT','Wt','S','Draft',' RndOvrl','Rk','GP','G','A','Pts','PlusMinus', 'PIM','TOI_G')

    def __init__(self, season, gametype):
        self._url = PLAYER_STATS_URL.format(season=season, gametype=GAMETYPE_MAP[gametype], viewname='bios', position='S')
    


class SummaryReader(StatsReader):
    '''Reads the Summary Report table from nhl.com''' 
    fieldnames = ('Number','Player','Team','Pos', 'GP','G','A','P','PlusmMinus', 'PIM','PP','SH','GW','OT','S', 'S_Perc','TOI_G', 'Sft_G'   'FO_Perc')

    def __init__(self, season, gametype):
        self._url = PLAYER_STATS_URL.format(season=season, gametype=GAMETYPE_MAP[gametype], viewname='summary', position='S')
    



READER_FACTORY_MAP = {
    'bios' : BiosReader,
    'summary' : SummaryReader
}


def reader(season, gametype='regular', report='bios'):
    '''Returns a StatsReader iterator. 

    Arguments:
    season - e.g. 20122013, 20112012
    gametype - one of 'regular' or 'playoff'
    report - one of 'bios' and 'summary'
    '''
    return READER_FACTORY_MAP[report](season, gametype)





