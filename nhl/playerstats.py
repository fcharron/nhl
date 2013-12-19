#!/usr/bin/env 

import re
import logging


from collections import namedtuple

import scraper
import reader


SkaterSummary = namedtuple("SkaterSummary", "number, player, team, pos, gp, g, a, pts, plusminus, pim, pp, sh, gw, ot, s, s_perc, toi_g, sft_g, fo_perc, id")

SkaterBios = namedtuple("SkaterBios", "number, player, team, pos, dob, birthcity, s_p, country, height, weight, s, draft, rnd, ovrl, rk, gp, g, a, pts, plusminus, pim, toi_g, id")

GoalieSummary = namedtuple("GoalieSummary", "number, player, team, gp, gs, w, l, ot, sa, ga, gaa, sv, sv_perc, so, g, a, pim, toi, id")
     
GoalieBios = namedtuple("GoalieBios", "number, player, team, dob, birthcity, s_p, country, height,weight, c, rk,draft,rnd,ovrl,gp,w, l, ot, gaa, svs, so, id")



TABLE_MAP = {
    'skaters' : {
        'summary' : SkaterSummary,
        'bios' : SkaterBios
    },
    'goalies' : {
        'bios' : GoalieBios,
        'summary' : GoalieSummary
    }
}


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


    def __init__(self, season, gametype, position, report):
        self.season = season
        self.gametype = gametype
        self.position = position
        self.report = report
        
        self.url = PLAYER_STATS_URL.format(season, *URL_MAP[position][report][gametype])


    def get_rowmap(self):
        return TABLE_MAP[self.position][self.report]


    def get_pagination_urls(self):
        '''Returns list of URLs for paginated tables at:
        http://www.nhl.com/ice/playerstats.htm
        ''' 

        NHL_BASE_URL = "http://www.nhl.com"


        #Load the first page
        soup = scraper.get_soup(self.url)

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


    def readtables(self):

        for page in self.get_pagination_urls():
            try: 
                soup = scraper.get_soup (page)
                table = soup.find('table', "stats")
            except:
                logging.warning("Could not read {}".format(page))
                raise StopIteration
            yield table 




    def readrows(self):

        for table in self.readtables():
            tbody = table.find("tbody")
            rows = tbody.find_all('tr')

            for row in rows:
                nhl_id = scraper.get_qp_from_href(row, "id", "/ice/player.htm")
                yield scraper.readdatacells(row) + [nhl_id] 




def reader(season, gametype="regular", position="skaters", report="bios"):
    return StatsTableReader(season, gametype, position, report)



if __name__ == '__main__':
    for p in reader("20122013"):
        print p





