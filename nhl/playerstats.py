#!/usr/bin/env python
'''
    PLAYER STATS

'''

import re
import hashlib
import logging
import urllib2
import urlparse

from collections import namedtuple
from bs4 import BeautifulSoup

from tablereader import TableReader
import formatters


class NhlPlayerStatsException(Exception):
    pass


PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'
GAMETYPES = {'regular' :2, 'playoff' :3 }
POSITIONS = {'skaters' :"S", 'goalies' :"G" }



SEASON_FORMAT = re.compile(r"(\d{8})")
NHL_ID_REGEX = re.compile(r"^/ice/player.htm")




SKATERSUMMARYWITHGT_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'gp' , 'g', 'a', 'p', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'gt', 'ot', 's', 
'sperc', 'toi_g', 'sft_g', 'foperc'

SKATER_SUMMARY_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'gp' , 'g', 'a', 'p', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'ot', 's', 'sperc', 'toi_g', 'sft_g', 'foperc'

GOALIESUMMARY_COLS = 'nhl_id', 'number', 'player', 'team', 'gp', 'gs', 'w', 'l', 'ot', 'sa', 'ga', 'gaa', 'sv', 'svperc', 'so', 'g', 'a', 'pim', 'toi'

GOALIESUMMARYWITHTIES_COLS = 'nhl_id', 'number', 'player', 'team', 'gp', 'gs', 'w', 'l', 't', 'ot', 'sa', 'ga', 'gaa', 'sv', 'svperc', 'so', 'g', 'a', 'pim', 'toi'

SKATER_BIOS_COLS = 'nhl_id', 'number', 'player', 'team', 'pos', 'dob', 'birthcity', 's_p', 'ctry', 'ht', 'wt', 's', 'draft', 'rnd', 'ovrl', 'rk', 'gp', 'g', 'a', 'pts', 'plusminus', 'pim', 'toi_g'

GOALIEBIOSWITHTIES_COLS = 'nhl_id','number','player','team','dob','birthcity','s_p','ctry','ht','wt','c','rk','draft','rnd','ovrl','gp','w','l','t','ot','gaa','svperc','so'

GOALIE_BIOS_COLS = 'nhl_id','number','player','team','dob','birthcity','s_p','ctry','ht','wt','c','rk','draft','rnd','ovrl','gp','w','l','ot','gaa','svperc','so'


SkaterSummaryWithGT = namedtuple("SkaterSummaryWithGT",
                                    SKATERSUMMARYWITHGT_COLS)
SkaterSummary = namedtuple("SkaterSummary", SKATER_SUMMARY_COLS)
SkaterBios = namedtuple("SkaterBios", SKATER_BIOS_COLS)


GoalieSummaryWithTies = namedtuple("GoalieSummaryWithTies",GOALIESUMMARYWITHTIES_COLS)
GoalieSummary = namedtuple("GoalieSummary", GOALIESUMMARY_COLS)

GoalieBiosWithTies = namedtuple("GoalieBiosWithTies", GOALIEBIOSWITHTIES_COLS)
GoalieBios = namedtuple("GoalieBios", GOALIE_BIOS_COLS)


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
    thead = table.find("thead")
    sig = hashlib.md5(u",".join(map(lambda td:unicode(td.string.strip().replace(" ","")), thead.find_all("th")))).hexdigest()
    return row_builders.get(sig, None)


class PlayerStats(object):

    def __init__(self):
        self._season = ""
        self._gametype = ""
        self._position = ""
        self._report = ""

        self.rowbuilder = None
        self.formatters = formatters.DEFAULT_FORMATTERS


    def season(self, s):
        if re.match(SEASON_FORMAT, s):
            self._season = s
        return self

    def gametype(self, gt):
        self._gametype = GAMETYPES.get(gt, "")  
        return self   

    def position(self, pos):        
        self._position = POSITIONS.get(pos, "")
        return self

    def report(self, r):
        if r in ('bios', 'summary'):
            self._report = r
        return self


    def readrows(self, limit):


        row_counter = 0
        for table in self.readtables():
            tbody = table.find("tbody")
            rows = tbody.find_all('tr')

            for row in rows:

                if row_counter == limit:
                    raise StopIteration

                anchor_tag = row.find("a", href=NHL_ID_REGEX)
                if anchor_tag:
                    qs = urlparse.urlparse(anchor_tag['href']).query
                    nhl_id = urlparse.parse_qs(qs).get("id", None)[0]
                else: 
                    nhl_id = None

                data = [nhl_id] + [td.string for td in row.find_all("td")] 

                formatted_data = [self.formatters[k](v) for k,v in zip(self.rowbuilder._fields, data)]

                yield self.rowbuilder._make(formatted_data)

                row_counter += 1


    
    def fetch(self, limit=None):
        '''Returns all table rows as one (potentially empty or very long) list
        '''
        return list(self.readrows(limit))

    
    def __iter__(self):
        return self.readrows(None)                


    def formatter(self, name, format_fnc):
        self.formatters[name] = format_fnc
        return self            


    def rawformat(self):
        self.formatters = formatters.RAW_FORMATTERS
        return self        



    def get_pagination_urls(self, all_anchors):
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


    def gettable(self, url):
        logging.info("Getting {}".format(url))
        try:
            html = urllib2.urlopen(url).read()
            soup = BeautifulSoup(html, 'lxml')
        except Exception as e:
            raise NhlPlayerStatsException("Failed to load {} : {}".format(url, e.message))
        return soup.find("table", "stats")


    def buildurl(self):
        if self._position == 'G' and self._report=='bios':
            report = 'goalieBios'
        else:
            report = self._report

        return PLAYER_STATS_URL.format(self._season, self._gametype,
                                        self._position, report)


    def readtables(self):

        url = self.buildurl()
        table = self.gettable(url)
        self.rowbuilder = make_rowbuilder(table)
        
        yield table

        for url in self.get_pagination_urls(table.select("tfoot.paging a")):
            table = self.gettable(url)

            yield table 



if __name__ == '__main__':

    ps = PlayerStats()
    ps.season("20132014")
    ps.gametype("playoff")
    ps.position("skaters")
    ps.report("summary")

    print len(ps.fetch())

    '''
    for n, s in enumerate(ps.fetch(32),1):
        print n,s

    '''