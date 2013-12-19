#!/usr/bin/env 

import re
import logging
import hashlib 

import tables
import scraper
import reader




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

    #Read table signatures as md5 hashes into a dict 
    table_signatures = {hashlib.md5(k).hexdigest() : v for k,v in tables.SIGNATURES}


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
            self.update_datamap(table)
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



def reader(season, gametype="regular", position="skaters", report="bios"):

    if gametype not in ('regular', 'playoff') or position not in ('skaters', 'goalies') or report not in ('bios', 'summary'):
        return None


    return StatsTableReader(season, gametype, position, report)



if __name__ == '__main__':
    reader = reader("20122013", "regular", "goalies", "bios")

    for p in reader.run(3):
        print p





