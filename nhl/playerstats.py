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


PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'
URL_MAP = {
    'skaters' : {
        'summary' : {
            'regular' : (2, "S", "summary"),
            'playoff' : (3, "S", "summary"),
        },
        'bios' : {
            'regular' : (2, "S", "bios"),
            'playoff' : (3, "S", "bios"),
        }

    },
    'goalies' : {
        'summary' : {
            'regular' : (2, "G", "summary"),
            'playoff' : (3, "G", "summary"),
        },
        'bios' : {
            'regular' : (2, "G", "goalieBios"),
            'playoff' : (3, "G", "goalieBios"),
        }

    }    
}


class SkaterSummaryWithGT(namedtuple("SkaterSummaryWithGT", "nhl_id, number, player, team, pos, gp , g, a, p, plusminus, pim, pp, sh, gw, gt, ot, s, sperc, toi_g, sft_g, foperc")):    
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = (int,int,str,str,int,int,int,int,int,int,int,int,int,float,str,float,float)
        return csl(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class SkaterSummary(namedtuple("SkaterSummary", "nhl_id, number, player, team, pos, gp , g, a, p, plusminus, pim, pp, sh, gw, ot, s, sperc, toi_g, sft_g, foperc")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = (int,int,str,str,str,int,int,int,int,int,int,int,int,int,int,int,float,str,float,float)
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class GoalieSummaryWithTies(namedtuple("GoalieSummaryWithTies", "nhl_id, number, player, team, gp, gs, w, l, t, ot, sa, ga, gaa, sv, svperc, so, g, a, pim, toi")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = (int,int,str,str,int,int,int,int,int,int,int,int,float,int,float,int,int,int,int,str)
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class GoalieSummary(namedtuple("GoalieSummary", "nhl_id, number, player, team, gp, gs, w, l, ot, sa, ga, gaa, sv, svperc, so, g, a, pim, toi")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = (int,int,str,str,int,int,int,int,int,int,int,float,int,float,int,int,int,int,str)
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class SkaterBios(namedtuple("SkaterBios", "nhl_id, number, player, team, pos, dob, birthcity, s_p, ctry, ht, wt, s, draft, rnd, ovrl, rk, gp, g, a, pts, plusminus, pim, toi_g")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = [str]*24
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class GoalieBiosWithTies(namedtuple("GoalieBiosWithTies", "nhl_id,number,player,team,dob,birthcity,s_p,ctry,ht,wt,c,rk,draft,rnd,ovrl,gp,w,l,t,ot,gaa,svperc,so")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = [str]*23
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


class GoalieBios(namedtuple("GoalieBios", "nhl_id,number,player,team,dob,birthcity,s_p,ctry,ht,wt,c,rk,draft,rnd,ovrl,gp,w,l,ot,gaa,svperc,so")):
    @classmethod
    def _from_rowdata(cls, nhl_id, data):
        mapper = [str]*22
        return cls(*[m(d) for m,d in zip(mapper,[nhl_id]+data)])


PLAYERSTATS_TABLE_SIGNATURES = [
(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,GT,OT,S,S%,TOI/G,Sft/G,FO%', SkaterSummaryWithGT),
(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,OT,S,S%,TOI/G,Sft/G,FO%', SkaterSummary),
(u',Player,Team,GP,GS,W,L,T,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', GoalieSummaryWithTies),
(u',Player,Team,GP,GS,W,L,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', GoalieSummary),
(u'#,Player,Team,Pos,DOB,BirthCity,S/P,Ctry,HT,Wt,S,Draft,Rnd,Ovrl,Rk,GP,G,A,Pts,+/-,PIM,TOI/G', SkaterBios),
(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,Sv%,SO', GoalieBiosWithTies),
(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,Sv%,SO', GoalieBios)
]

NHL_ID_REGEX = re.compile(r"^/ice/player.htm")

class PlayerStats(object):

    #Read table signatures as md5 hashes into a dict 
    table_signatures = {hashlib.md5(k).hexdigest() : v for k,v in PLAYERSTATS_TABLE_SIGNATURES}


    def __init__(self, season, gametype, position, report):
        self.season = season
        self.gametype = gametype
        self.position = position
        self.report = report
        
        self.datamap = None


    def update_datamap(self, table):
        thead = table.find("thead")
        sig = hashlib.md5(u",".join(map(lambda td:unicode(td.string.strip().replace(" ","")), thead.find_all("th")))).hexdigest()
        self.datamap = self.table_signatures[sig]



    def get_pagination_urls(self, soup):
        '''Returns list of URLs for paginated tables at:
        http://www.nhl.com/ice/playerstats.htm
        ''' 

        #Get all anchors with page links
        pages = soup.find('div', 'pages')
        all_anchors = pages.find_all("a")
        number_of_anchors = len(all_anchors)

        #If no pages, return empty list
        if number_of_anchors < 1:
            return list()
        
        #Get the last page anchor
        last_anchor = all_anchors[number_of_anchors-1]
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

        return urls 


    def getsoup(self, url):
        html = urllib2.urlopen(url).read()
        return BeautifulSoup(html, 'lxml')


    def readtables(self):

        url = PLAYER_STATS_URL.format(
                self.season, 
                *URL_MAP[self.position][self.report][self.gametype])

        try:
            soup = self.getsoup(url)
        except:
            logging.error("Failed to load from {}".format(url))
            raise StopIteration
  
        for page in self.get_pagination_urls(soup):
            try: 
                soup = self.getsoup(page)
                table = soup.find("table", "stats")
            except:
                logging.warning("Could not read {}".format(page))
                raise StopIteration
            self.update_datamap(table)
            yield table 




    def readrows(self):

        for table in self.readtables():
            tbody = table.find("tbody")
            rows = tbody.find_all('tr')

            for row in rows:
                
                anchor_tag = row.find("a", href=NHL_ID_REGEX)
                if anchor_tag:
                    qs = urlparse.urlparse(anchor_tag['href']).query
                    nhl_id = urlparse.parse_qs(qs).get("id", None)[0]
                else: 
                    nhl_id = None

                data = [td.string for td in row.find_all("td")]

                yield self.datamap._from_rowdata(nhl_id, data)


def stats(season, gametype="regular", position="skaters", report="bios"):

    if gametype not in ('regular', 'playoff') or position not in ('skaters', 'goalies') or report not in ('bios', 'summary'):
        return None

    return TableReader(PlayerStats(season, gametype, position, report))    


if __name__ == '__main__':

     for s in stats("20132014", "regular", "goalies", "bios"):
        print s