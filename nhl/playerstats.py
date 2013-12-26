#!/usr/bin/env python
'''
Reads Player stats tables at nhl.com. 

Example usage

    ps = PlayerStats()
    ps.season("20132014")
    ps.gametype("regular")
    ps.position("skaters")
    ps.report("bios")

    for row in ps:
        print row


'''

import re
import logging
import urllib2
import urlparse
from collections import namedtuple

from bs4 import BeautifulSoup


import formatters

DATA_MAP = {
    'integers' : ('gp', 'g', 'a', 'p', 'pts', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'gt', 'ot', 'nhl_id', 'number', 'ppg', 'shg', 'gwg', 'gs', 'ga', 'sv', 'l', 'w', 't', 'sa', 'so', 'ht', 'wt', 'draft', 'rnd', 'ovrl'),
    'floats' : ('sperc', 'foperc', 'gaa', 'svperc', 'sftg'),
    'minutes' : ('toig', 'toi', 'min')
}
formatter = formatters.Formatter(DATA_MAP)


class NhlPlayerStatsException(Exception):
    pass



class PlayerStatsTable:
    '''Models a player stats table on nhl.com/ice. It can be paginated.

    Example usage
    table = PlayerStatsTable(url)

    table.columns

    for row in table.rows():
        do something

    '''


    #regex for finding a URL with player id in querystring
    NHL_ID_REGEX = re.compile(r"^/ice/player.htm")


    @staticmethod
    def get(url):
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')
            return soup.find("table", "stats")
        except Exception as e:
            raise NhlPlayerStatsException("Failed to load {} : {}".format(url, e.message))


    @staticmethod
    def get_nhlid_from_tablerow(tr):        
        #Get player ID from href inside the row

        anchor_tag = tr.find("a", href=PlayerStatsTable.NHL_ID_REGEX)
        if anchor_tag:
            qs = urlparse.urlparse(anchor_tag['href']).query
            return urlparse.parse_qs(qs).get("id", None)[0]


    @staticmethod
    def cleanup_columnname(name):
        return name.strip().lower().replace("+/-", "plusminus").replace("%", "perc").replace("/","").replace("#","number").replace(" ","")


    def __init__(self, url):
        self.url = url
        self.pageone = PlayerStatsTable.get(url)
        self._update_pageurls()            
        self._update_columns()


    def _update_pageurls(self):  
        ''''''         
        
        self._page_urls = []

        pages_div = self.pageone.find("div", "pages")


        #Check for empty table
        if pages_div is None:
            return 

        #Check for one page table
        page_anchors = pages_div.find_all("a")
        if len(page_anchors) < 1:
            #One page table
            self._page_urls.append(self.url)
            return


        #Get the last page anchor
        last_anchor = page_anchors[-1]
        last_anchor_href = last_anchor.get("href")
        
        #Get the number of the last page
        pattern = re.compile(r"(\d+)")
        number_of_pages =  pattern.findall(last_anchor_href)[-1]

        #Load all pages
        NHL_BASE_URL = "http://www.nhl.com"
        for p in range(1,int(number_of_pages)+1):
            page_url = NHL_BASE_URL + last_anchor_href.replace("pg="+number_of_pages,"pg="+str(p) )
            self._page_urls.append(page_url)



    def _update_columns(self):
        thead = self.pageone.find("thead")
        self._columns = ['nhl_id', 'number'] + map(
                        PlayerStatsTable.cleanup_columnname, 
                        [th.string for th in thead.find_all("th")])[1:]


    @property        
    def columns(self):
        return self._columns        


    def rows(self):

        for url in self._page_urls:
            table = PlayerStatsTable.get(url)

            tbody = table.find("tbody")

            if tbody is None:
                raise StopIteration

            for tr in tbody.find_all('tr'):

                nhl_id = PlayerStatsTable.get_nhlid_from_tablerow(tr)

                data = [nhl_id] + [td.string for td in tr.find_all("td")]

                yield [formatter.format(k,v) for k,v in zip(self.columns, data)]



class PlayerStatsReader(object):
    '''
    Reads a table, row by row up to a limit, and converts all rows into a PlayerStats named tuple. 

    '''


    def __init__(self, url, limit):
        self.table = PlayerStatsTable(url)
        self.limit = limit  


    def readrows(self):
        '''Reads all or a limited numbers of rows from the table'''


        #Create rowdata class from table columns
        rowdataclass = namedtuple("PlayerStats", self.table.columns)

        #Get pages, if more
        row_counter = 0
        for row in self.table.rows():

            if row_counter == self.limit:
                raise StopIteration

            yield rowdataclass._make(row)

            row_counter += 1

    
    def __iter__(self):
        return self.readrows()                





class Query(object):

    #Format for URL to get tables
    PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'
    GAMETYPES = {'regular' :2, 'playoff' :3 }
    POSITIONS = {'skaters' :"S", 'goalies' :"G" }

    @staticmethod
    def is_valid_season(s):
        '''Returns True for a valid season (e.g. 20132014)'''
        return re.match(r"(\d{8})", s)


    def __init__(self):
        self._season = ""
        self._gametype = ""
        self._position = ""
        self._report = ""


    def season(self, s):
        '''Sets the desired season on the format, YYYYYYYY'''
        if Query.is_valid_season(s):
            self._season = s
        return self

    def gametype(self, gt):
        '''Sets gametype to 'regular' or 'playoff'''
        self._gametype = Query.GAMETYPES.get(gt, "")  
        return self   

    def position(self, pos):        
        '''Sets position to 'skaters' or 'goalies'''
        self._position = Query.POSITIONS.get(pos, "")
        return self

    def report(self, r):
        '''Sets report to 'bios' or 'summary'''
        if r in ('bios', 'summary'):
            self._report = r
        return self


    def buildurl(self):
        '''Builds the URL based on parameters''' 
        if self._position == 'G' and self._report=='bios': 
            report = 'goalieBios' #This is not nice, but who it works
        else:
            report = self._report

        return Query.PLAYER_STATS_URL.format(self._season, self._gametype,
                                        self._position, report)


    def run(self, limit=None):
        '''Executes the query and returns an iterator'''

        url = self.buildurl()
        return PlayerStatsReader(url, limit)


    def fetch(self, limit=None):
        return list(self.run(limit))



if __name__ == '__main__':

    q = Query()
    q.season("20132014")
    q.gametype("regular")
    q.position("goalies")
    q.report("bios")

    for row in q.run():
        print row

    