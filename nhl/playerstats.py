#!/usr/bin/env 

import re
import logging


from collections import namedtuple

import scraper

PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'



SkaterSummary = namedtuple("SkaterSummary", "number, player, team, pos, gp, g, a, pts, plusminus, pim, pp, sh, gw, ot, s, s_perc, toi_g, sft_g, fo_perc, id")

SkaterBios = namedtuple("SkaterBios", "number, player, team, pos, dob, birthcity, s_p, country, height, weight, s, draft, rnd, ovrl, rk, gp, g, a, pts, plusminus, pim, toi_g, id")

GoalieSummary = namedtuple("GoalieSummary", "number, player, team, gp, gs, w, l, ot, sa, ga, gaa, sv, sv_perc, so, g, a, pim, toi, id")
     
GoalieBios = namedtuple("GoalieBios", "number, player, team, dob, birthcity, s_p, country, height,weight, c, rk,draft,rnd,ovrl,gp,w, l, ot, gaa, svs, so, id")



TABLE_MAP = {
    'skaters' : {
        'summary' : ("S","summary", SkaterSummary),
        'bios' : ("S", "bios", SkaterBios)
    },
    'goalies' : {
        'bios' : ("G", "goalieBios", GoalieBios),
        'summary' : ("G", "summary", GoalieSummary)
    }
}




def get_pagination_urls(url):
    '''Returns list of URLs for paginated tables at:
    http://www.nhl.com/ice/playerstats.htm
    ''' 

    NHL_BASE_URL = "http://www.nhl.com"


    #Load the first page
    soup = scraper.get_soup(url)

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


def readtables(urls):

    for page in urls:
        try: 
            soup = scraper.get_soup (page)
            table = soup.find('table', "stats")
        except:
            logging.warning("Could not read {}".format(page))
            raise StopIteration
        yield table 


def readdatacells(row):

    tds = row.find_all('td')
    
    data = []  
    for td in tds:
        try: 
            data.append(td.string.strip())
        except:
            data.append(None)

    nhl_id = scraper.get_qp_from_href(row, "id", "/ice/player.htm")
    data.append(nhl_id)

    return data 



def readrows(urls):

    for table in readtables(urls):
        tbody = table.find("tbody")
        if tbody:
            rows = tbody.find_all('tr')
        else:
            rows = table.find_all("tr")[1:-1]

        for row in rows:
            yield readdatacells(row) 


class StatsTableReader(object):

    def __init__(self, urls, datamapper):
        self.urls = urls
        self.datamapper = datamapper
        


    def run(self, limit=None):

        row_counter = 0
        for row in readrows(self.urls):
            if row_counter == limit:
                raise StopIteration
            
            yield self.datamapper._make(row)
            
            row_counter += 1

    
    def fetch(self, limit=None):
        '''Returns the stats as a list'''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()



def reader(season, gametype="regular", position="skaters", report="bios"):

    gametype_id = {'regular' : 2, 'playoff' : 3}

    pos, viewname, mapper = TABLE_MAP[position][report]

    url = PLAYER_STATS_URL.format(season, gametype_id[gametype], pos, viewname)
    urls = get_pagination_urls(url)

    return StatsTableReader(urls, mapper)



if __name__ == '__main__':
    for p in reader("20122013"):
        print p





