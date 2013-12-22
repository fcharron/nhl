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
import hashlib
import logging
import urllib2
import urlparse
from collections import namedtuple

from bs4 import BeautifulSoup

import formatters

class NhlPlayerStatsException(Exception):
    pass


#Format for URL to get tables
PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'
GAMETYPES = {'regular' :2, 'playoff' :3 }
POSITIONS = {'skaters' :"S", 'goalies' :"G" }



#YYYYYYYY, e.g. 20122013
SEASON_FORMAT = re.compile(r"(\d{8})") 


#regex for finding a URL with player id in querystring
NHL_ID_REGEX = re.compile(r"^/ice/player.htm")


'''
Two kinds of reports are supported: 

- Summary
- Bios

Some older tables include tie games, which is no longer supported. 

'''

SKATERSUMMARYWITHGT_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'gp' , 'g', 'a', 'p', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'gt', 'ot', 's', 
'sperc', 'toi_g', 'sft_g', 'foperc'

SKATER_SUMMARY_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'gp' , 'g', 'a', 'p', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'ot', 's', 'sperc', 'toi_g', 'sft_g', 'foperc'

GOALIESUMMARY_COLS = 'nhl_id', 'number', 'player', 'team', 'gp', 'gs', 'w', 'l', 'ot', 'sa', 'ga', 'gaa', 'sv', 'svperc', 'so', 'g', 'a', 'pim', 'toi'

GOALIESUMMARYWITHTIES_COLS = 'nhl_id', 'number', 'player', 'team', 'gp', 'gs', 'w', 'l', 't', 'ot', 'sa', 'ga', 'gaa', 'sv', 'svperc', 'so', 'g', 'a', 'pim', 'toi'

SKATER_BIOS_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'dob', 'birthcity', 's_p', 'ctry', 'ht', 'wt', 's', 'draft', 'rnd', 'ovrl', 'rk', 'gp', 'g', 'a', 'pts', 'plusminus', 'pim', 'toi_g'

GOALIEBIOSWITHTIES_COLS = 'nhl_id','number','player','team','dob','birthcity','s_p','ctry','ht','wt','c','rk','draft','rnd','ovrl','gp','w','l','t','ot','gaa','svperc','so'

GOALIE_BIOS_COLS = 'nhl_id','number','player','team','dob','birthcity','s_p','ctry','ht','wt','c','rk','draft','rnd','ovrl','gp','w','l','ot','gaa','svperc','so'

'''

Data is copied into relevant 'namedtuple'. A namedtuple is a small class. 

'''
SkaterSummaryWithGT = namedtuple("SkaterSummaryWithGT",
                                    SKATERSUMMARYWITHGT_COLS)
SkaterSummary = namedtuple("SkaterSummary", SKATER_SUMMARY_COLS)
SkaterBios = namedtuple("SkaterBios", SKATER_BIOS_COLS)


GoalieSummaryWithTies = namedtuple("GoalieSummaryWithTies",GOALIESUMMARYWITHTIES_COLS)
GoalieSummary = namedtuple("GoalieSummary", GOALIESUMMARY_COLS)

GoalieBiosWithTies = namedtuple("GoalieBiosWithTies", GOALIEBIOSWITHTIES_COLS)
GoalieBios = namedtuple("GoalieBios", GOALIE_BIOS_COLS)

'''
To detect what kind of table we are reading, we look what's in the header row and look up the corresponding table. 
'''
TABLE_SIGNATURES = [
(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,GT,OT,S,S%,TOI/G,Sft/G,FO%', SkaterSummaryWithGT),
(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,OT,S,S%,TOI/G,Sft/G,FO%', SkaterSummary),
(u',Player,Team,GP,GS,W,L,T,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', GoalieSummaryWithTies),
(u',Player,Team,GP,GS,W,L,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', GoalieSummary),
(u'#,Player,Team,Pos,DOB,BirthCity,S/P,Ctry,HT,Wt,S,Draft,Rnd,Ovrl,Rk,GP,G,A,Pts,+/-,PIM,TOI/G', SkaterBios),
(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,Sv%,SO', GoalieBiosWithTies),
(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,Sv%,SO', GoalieBios)
]

#Read table signatures as md5 hashes into a dict 
row_builders = {hashlib.md5(k).hexdigest() : v for k,v in TABLE_SIGNATURES}


def make_rowbuilder(table):
    '''Returns the relevant namedtuple for the tavble'''
    thead = table.find("thead")
    sig = hashlib.md5(u",".join(map(lambda td:unicode(td.string.strip().replace(" ","")), thead.find_all("th")))).hexdigest()
    return row_builders.get(sig, None)


class PlayerStats(object):
    '''
    Represents the playerstats tables at nh.com/ice/playerstats. A table is defined by season, gametype, position and report. For example, 'bios for skaters in 20122013'.
    The defaults are what's currently the default at nhl.com/ice/playerstats. 

    When the data is read it is formatted (e.g. converted from string to int) according to Formatters defined in formatters.py
    A default formatting is done for all data, but you can define your own functions for formatting the data. 


    The preferred way of reading the table is to use this class as an iterator: 

    for row in PlayerStats():
        print row


    Or by calling 'readrows' directly with a limit. 

    for row in PlayerStats().readrows(42):
        print row

    
    If you need the complete list at once into memory (not recommended), use the fetch() method. 

    all_skaters = PlayerStats().position("skaters").fetch()


    '''

    def __init__(self):
        self._season = ""
        self._gametype = ""
        self._position = ""
        self._report = ""

        self.rowbuilder = None
        self.formatters = formatters.DEFAULT_FORMATTERS


    def season(self, s):
        '''Sets the desired season on the format, YYYYYYYY'''
        if re.match(SEASON_FORMAT, s):
            self._season = s
        return self

    def gametype(self, gt):
        '''Sets gametype to 'regular' or 'playoff'''
        self._gametype = GAMETYPES.get(gt, "")  
        return self   

    def position(self, pos):        
        '''Sets position to 'skaters' or 'goalies'''
        self._position = POSITIONS.get(pos, "")
        return self

    def report(self, r):
        '''Sets report to 'bios' or 'summary'''
        if r in ('bios', 'summary'):
            self._report = r
        return self


    def readrows(self, limit):
        '''Reads all or a limited numbers of rows from the table'''

        row_counter = 0
        for table in self._readtables():
            tbody = table.find("tbody")
            rows = tbody.find_all('tr')

            for row in rows:

                if row_counter == limit:
                    raise StopIteration

                #Get player ID from href inside the row
                anchor_tag = row.find("a", href=NHL_ID_REGEX)
                if anchor_tag:
                    qs = urlparse.urlparse(anchor_tag['href']).query
                    nhl_id = urlparse.parse_qs(qs).get("id", None)[0]
                else: 
                    nhl_id = None

                #Add ID at the beginning of the data                    
                data = [nhl_id] + [td.string for td in row.find_all("td")] 

                #Apply formatters on all data
                formatted_data = [self.formatters[k](v) for k,v in zip(self.rowbuilder._fields, data)]

                #Create the row and  return
                yield self.rowbuilder._make(formatted_data)

                row_counter += 1


    
    def fetch(self, limit=None):
        '''Returns all table rows as one (potentially empty or very long) list
        '''
        return list(self.readrows(limit))

    
    def __iter__(self):
        return self.readrows(None)                


    def formatter(self, name, format_fnc):
        '''Set a formatting function to  the given data item. 

        - name  - Name of data cell
        - format_fnc - A function that will be called with the raw data from the cell with the given name.


        Example, converts 'dob', date of birth to datetime. 
        ps = PlayerStats()
        ps.formatters("dob", lambda x: datetime.datetime.strptime(x,"%m %d '%y"))

        '''
        self.formatters[name] = format_fnc
        return self            


    def rawformat(self):
        '''Returns all data is raw format, i.e. not formatted at all. '''
        self.formatters = formatters.RAW_FORMATTERS
        return self        



    def _get_pagination_urls(self, all_anchors):
        '''Returns list of URLs for paginated tables at:
        http://www.nhl.com/ice/playerstats.htm
        ''' 

        if len(all_anchors) < 1:
            return []

        #Get the last page anchor
        last_anchor = all_anchors[-1]
        last_anchor_href = last_anchor.get("href")
        
        #Get the number of the last page
        pattern = re.compile(r"(\d+)")
        number_of_pages =  pattern.findall(last_anchor_href)[-1]

        #Load all pages
        NHL_BASE_URL = "http://www.nhl.com"
        urls = []
        for p in range(1,int(number_of_pages)+1):
            page_url = NHL_BASE_URL + last_anchor_href.replace("pg="+number_of_pages,"pg="+str(p) )
            urls.append(page_url)

        return urls[1:] 


    def _gettable(self, url):
        '''Returns the stats table from the given URL'''
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')
        except Exception as e:
            raise NhlPlayerStatsException("Failed to load {} : {}".format(url, e.message))
        return soup.find("table", "stats")


    def _buildurl(self):
        '''Builds the URL based on parameters''' 
        if self._position == 'G' and self._report=='bios': 
            report = 'goalieBios' #This is not nice, but who it works
        else:
            report = self._report

        return PLAYER_STATS_URL.format(self._season, self._gametype,
                                        self._position, report)


    def _readtables(self):
        '''Reads all tables; often the table is paginated into several tables on different URLs.''' 

        url = self._buildurl()
        table = self._gettable(url)
        self.rowbuilder = make_rowbuilder(table)
        
        yield table

        for url in self._get_pagination_urls(table.select("tfoot.paging a")):
            table = self._gettable(url)

            yield table 



if __name__ == '__main__':

    ps = PlayerStats()
    ps.season("20132014")
    ps.gametype("regular")
    ps.position("skaters")
    ps.report("bios")

    for row in ps:
        print row

    