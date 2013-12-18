#!/usr/bin/env 

'''Career Stats 
http://www.nhl.com/ice/player.htm


'''

from collections import namedtuple

import reader
import scraper

PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"


GoalieCareerStatsRow = namedtuple("GoalieCareerStatsRow", "season, team, gp, g, w, l, t, ot, so, ga, sa, svs, gaa, min, id")

SkaterCareerStatsRow = namedtuple("SkaterCareerStatsRow", "season, team, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc, id")



class CareerStatsReader(reader.AbstractReader):
    '''Reads Career Stats from player's bio page''' 

    _tables_headers = {
        "regular" : "CAREER REGULAR SEASON STATISTICS", 
        "playoff" : "CAREER PLAYOFF STATISTICS"
        }


    def __init__(self, nhl_id, gametype):
        self.nhl_id = nhl_id
        self.gametype = gametype
        
        self.rowdata = SkaterCareerStatsRow


    def get_row_id(self, row):
        return scraper.get_qp_from_href(row, "tm", "/ice/playersearch.htm")



    def readtables(self):
        '''Returns list of tables to be read'''

        url = PLAYER_URL.format(str(self.nhl_id))
        
        soup = scraper.get_soup(url)

        table_header = soup.find("h3",
                        text=self._tables_headers[self.gametype])

        return [table_header.next_sibling] #We only have one table



def career_reader(nhl_id, gametype):
    return CareerStatsReader(nhl_id, gametype)


