#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''nhl.py

A module for reading player stats from nhl.com. 

Example usage: 

import nhl

nhl_reader = reader("20132014", gametype="regular", report='bios')

for player in nhl_reader:
    print player


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

    _fields = ()

    @property
    def fieldnames(self):
        return [field[0] for field in self._fields]


    def _readrow(self, stats_table):
        '''Yields one row from the table as a list'''
        for tr in stats_table.find('tbody').findAll('tr'):
            
            tds = tr.findAll('td') 
            
            row = {}     
            for i, d in enumerate(self._fields):
                value = tds[i].string    

                if value:
                    row[d[0]] = d[1](value)
                else:
                    row[d[0]] = None #Empty cells

            yield row


    def _get_all_pages(self):
        '''Yields URLs for player stats pages''' 

        #Load the first page
        soup = get_soup(self._url)

        #Get all anchors with page links
        pages = soup.find('div', 'pages')
        all_anchors = pages.find_all("a")
        number_of_anchors = len(all_anchors)

        #Check in case there are no pages
        if number_of_anchors < 1:
            raise StopIteration
        
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
                yield row


    def execute(self):
        '''Returns the stats as a list'''
        return list(self)



GAMETYPE_MAP = {
    'regular' : 2,
    'playoff' : 3
}


def yesno(v):
    if v=='Y':
        return True
    elif v=='N':
        return False
    else:
        return None


class BiosReader(StatsReader):
    '''Reads the Bios Report table from nhl.com''' 
    _fields = (('Number',int),('Player',unicode),('Team',unicode),('Pos',unicode),('DOB',unicode),('BirthCity',unicode),('S_P',unicode), ('Ctry',unicode), ('HT',int),('Wt',int),('S',unicode),('Draft',unicode),('Rnd',int),('Ovrl',int),('Rk',yesno),('GP',int),('G',int),('A',int),('Pts',int),('PlusMinus',int),('PIM',int),('TOI_G',unicode))

    def __init__(self, season, gametype):
        self._url = PLAYER_STATS_URL.format(season=season, gametype=GAMETYPE_MAP[gametype], viewname='bios', position='S')
    


class SummaryReader(StatsReader):
    '''Reads the Summary Report table from nhl.com''' 

    _fields = (('Number',int),('Player', unicode),('Team',unicode),('Pos',unicode),('GP',int),('G',int),('A',int),('P',int),('PlusMinus',int),('PIM',int),('PP',int),('SH',int),('GW',int),('OT',int),('S',int), ('S_Perc',float),('TOI_G',unicode),('Sft_G',float),('FO_Perc',float))


    def __init__(self, season, gametype):
        self._url = PLAYER_STATS_URL.format(season=season, gametype=GAMETYPE_MAP[gametype], viewname='summary', position='S')
    



READER_FACTORY_MAP = {
    'bios' : BiosReader, 
    'summary' : SummaryReader
    }



def reader(season, gametype='regular', report='summary'):
    '''Returns a StatsReader iterator. 

    Arguments:
    season - e.g. 20122013, 20112012
    gametype - one of 'regular' or 'playoff'
    report - one of 'bios' and 'summary'
    '''
    return READER_FACTORY_MAP[report](season, gametype)



if __name__ == '__main__':

    nhl_reader = reader("20132014", gametype="regular", report='summary')

    print nhl_reader.fieldnames

    for player in nhl_reader:
        print player


    