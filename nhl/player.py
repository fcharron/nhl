#!/usr/bin/env 

'''Career Stats 
http://www.nhl.com/ice/player.htm


'''
import re
import scraper
import reader

PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"

from collections import namedtuple

TABLE_MAP = {
    'regular' : {
        'skater' : namedtuple("SkaterCareerStatsRegular", "season, team, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc, team_id, gametype"),
        'goalie' : namedtuple("GoalieCareerStatsRegular", "season, team, gp, w, l, t, ot, so, ga, sa, svs, gaa, min, team_id, gametype")
    },
    'playoff' : {
        'skater' : namedtuple("SkaterCareerStatsPlayoff", "season, team, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc, team_id, gametype"),
        'goalie' : namedtuple("GoalieCareerStatsPlayoff", "season, team, gp, w, l, so, ga, sa, svs, gaa, min, team_id, gametype")    
    }
}


class CareerStatsReader(reader.TableRowsIterator):

    def __init__(self, url):
        self.url = url     
        self.position = "skater" #default
        self.gametype = "regular" #default

        self.datamap = None


    def update_datamap(self):
        self.datamap = TABLE_MAP[self.gametype][self.position]


    def get_careerstats_tables(self):
        '''Returns list of tables to be read'''

        soup = scraper.get_soup(self.url)

        if soup.find(id="tombstone").find(text=re.compile("Goalie")):
            self.position = "goalie"


        CAREER_TABLES = {
            'regular' : "CAREER REGULAR SEASON STATISTICS",
            'playoff' :  "CAREER PLAYOFF STATISTICS"
        }

        for table_name in CAREER_TABLES:

            h3 = soup.find("h3", text=CAREER_TABLES[table_name])

            self.gametype = table_name 
            
            self.update_datamap()           

            yield h3.next_sibling


    def readrows(self):

        for table in self.get_careerstats_tables():
            rows = table.find_all("tr")[1:-1]

            for row in rows:
                team_id = scraper.get_qp_from_href(row, "tm", "/ice/playersearch.htm")

                yield scraper.readdatacells(row) + [team_id, self.gametype]





def reader(nhl_id):

    url = PLAYER_URL.format(str(nhl_id))

    return CareerStatsReader(url)



if __name__ == '__main__':

    for p in reader(8445386):
        print p
