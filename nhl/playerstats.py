#!/usr/bin/env python
'''
    PLAYER STATS

'''

import re
import hashlib
import logging

from collections import namedtuple

from nhlreader import getsoup, get_qp_from_href, get_rowdata_as_list

PlayerStatsRow = namedtuple("PlayerStatsRow", "season, gametype, nhl_id, data")

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

PLAYERSTATS_TABLE_SIGNATURES = [

(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,GT,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary", 
        u"Number, Player, Team, Pos, GP , G, A, P, PlusMinus, PIM, PP, SH, GW, GT, OT, S, SPerc, TOI_G, Sft_G, FOPerc")),

(u',Player,Team,GP,GS,W,L,T,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary",
        u"Number, Player, Team, GP, GS, W, L, T, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI")),

(u',Player,Team,GP,GS,W,L,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary2", 
        u"Number, Player, Team, GP, GS, W, L, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI")),

(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary2",
        u"Number, Player, Team, Pos, GP, G, A, P, PlusMinus, PIM, PP, SH, GW, OT, S, SPerc, TOI_G, Sft_G, FOPerc")),

(u'#,Player,Team,Pos,DOB,BirthCity,S/P,Ctry,HT,Wt,S,Draft,Rnd,Ovrl,Rk,GP,G,A,Pts,+/-,PIM,TOI/G', namedtuple("SkaterBios",
    u"Number, Player, Team, Pos, DOB, BirthCity, S_P, Ctry, HT, Wt, S, Draft, Rnd, Ovrl, Rk, GP, G, A, Pts, PlusMinus, PIM, TOI_G")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,Sv%,SO', namedtuple("GoalieBios1", "Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,SvPerc,SO")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,Sv%,SO', namedtuple("GoalieBios2","Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,SvPerc,SO"))

]

class PlayerStatsTable(object):

    #Read table signatures as md5 hashes into a dict 
    table_signatures = {hashlib.md5(k).hexdigest() : v for k,v in PLAYERSTATS_TABLE_SIGNATURES}


    def __init__(self, season, gametype, position, report):
        self.season = season
        self.gametype = gametype
        self.position = position
        self.report = report
        
        self.url = PLAYER_STATS_URL.format(season, *URL_MAP[position][report][gametype])

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


    def readtables(self):

        soup = getsoup(self.url)

        for page in self.get_pagination_urls(soup):
            try: 
                soup = getsoup(page)
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
                nhl_id = get_qp_from_href(row, "id", "/ice/player.htm")
                yield PlayerStatsRow(self.season, self.gametype, nhl_id, self.datamap._make(get_rowdata_as_list(row)))


if __name__ == '__main__':

     for s in PlayerStatsTable("20132014", "regular", "skaters", "bios").readrows():
        print s