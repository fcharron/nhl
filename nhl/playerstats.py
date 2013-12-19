#!/usr/bin/env 

import re
import logging
import hashlib 

from collections import namedtuple

import scraper
import reader


'''
There are many different kinds of tables for Player Stats, the available stats is different from year to year.

In order to find the correct table, we detect the table 'signature', a string of all column namne. Based on that, we look up the correct table.  
'''
TABLE_SIGNATURES = [
(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,GT,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary", 
        u"Number, Player, Team, Pos, GP , G, A, P, PlusMinus, PIM, PP, SH, GW, GT, OT, S, SPerc, TOI_G, Sft_G, FOPerc, ID")),

(u',Player,Team,GP,GS,W,L,T,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary",
        u"Number, Player, Team, GP, GS, W, L, T, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI, ID")),

(u',Player,Team,GP,GS,W,L,OT,SA,GA,GAA,Sv,Sv%,SO,G,A,PIM,TOI', 
    namedtuple("GoalieSummary2", 
        u"Number, Player, Team, GP, GS, W, L, OT, SA, GA, GAA, Sv, SvPerc, SO, G, A, PIM, TOI, ID")),

(u',Player,Team,Pos,GP,G,A,P,+/-,PIM,PP,SH,GW,OT,S,S%,TOI/G,Sft/G,FO%', 
    namedtuple("SkaterSummary2",
        u"Number, Player, Team, Pos, GP, G, A, P, PlusMinus, PIM, PP, SH, GW, OT, S, SPerc, TOI_G, Sft_G, FOPerc, ID")),

(u'#,Player,Team,Pos,DOB,BirthCity,S/P,Ctry,HT,Wt,S,Draft,Rnd,Ovrl,Rk,GP,G,A,Pts,+/-,PIM,TOI/G', namedtuple("SkaterBios",
    u"Number, Player, Team, Pos, DOB, BirthCity, S_P, Ctry, HT, Wt, S, Draft, Rnd, Ovrl, Rk, GP, G, A, Pts, PlusMinus, PIM, TOI_G, ID")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,Sv%,SO', namedtuple("GoalieBios1", "Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,T,OT,GAA,SvPerc,SO,ID")),

(u'#,Player,Team,DOB,BirthCity,S/P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,Sv%,SO', namedtuple("GoalieBios2","Number,Player,Team,DOB,BirthCity,S_P,Ctry,HT,Wt,C,Rk,Draft,Rnd,Ovrl,GP,W,L,OT,GAA,SvPerc,SO,ID"))
]




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


class StatsTableReader(reader.TableRowsIterator):

    table_signatures = {}


    def __init__(self, season, gametype, position, report):
        self.season = season
        self.gametype = gametype
        self.position = position
        self.report = report
        
        self.url = PLAYER_STATS_URL.format(season, *URL_MAP[position][report][gametype])

        self.table = None


    @property         
    def row_datamap(self):
        thead = self.table.find("thead")
        sig = hashlib.md5(u",".join(map(lambda td:unicode(td.string.strip().replace(" ","")), thead.find_all("th")))).hexdigest()
        return self.table_signatures[sig]



    def get_pagination_urls(self):
        '''Returns list of URLs for paginated tables at:
        http://www.nhl.com/ice/playerstats.htm
        ''' 

        #Get all anchors with page links
        pages = self.soup.find('div', 'pages')
        all_anchors = pages.find_all("a")
        number_of_anchors = len(all_anchors)
        
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

        for page in self.get_pagination_urls():
            try: 
                soup = scraper.get_soup (page)
                table = soup.find('table', "stats")
            except:
                logging.warning("Could not read {}".format(page))
                raise StopIteration
            self.table = table
            yield table 




    def readrows(self):

        try:
            self.soup = scraper.get_soup(self.url)
        except:
            raise StopIteration

        for table in self.readtables():
            tbody = table.find("tbody")
            rows = tbody.find_all('tr')

            for row in rows:
                nhl_id = scraper.get_qp_from_href(row, "id", "/ice/player.htm")
                yield scraper.readdatacells(row) + [nhl_id] 


for sig in TABLE_SIGNATURES:
    StatsTableReader.table_signatures[hashlib.md5(sig[0]).hexdigest()] = sig[1]


def reader(season, gametype="regular", position="skaters", report="bios"):

    if gametype not in ('regular', 'playoff') or position not in ('skaters', 'goalies') or report not in ('bios', 'summary'):
        return None


    return StatsTableReader(season, gametype, position, report)



if __name__ == '__main__':
    reader = reader("20122013", "regular", "goalies", "bios")

    for p in reader.run(3):
        print p





