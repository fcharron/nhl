#!/usr/bin/env 

'''
    Player Stats Reader
    http://www.nhl.com/ice/playerstats.htm

'''

import logging
from collections import namedtuple

import scraper
import reader


PLAYER_STATS_URL = 'http://www.nhl.com/ice/playerstats.htm?season={}&gameType={}&team=&position={}&country=&status=&viewName={}'



SkaterSummaryRow = namedtuple("SkaterSummaryRow", "number, player, team, pos, gp, g, a, pts, plusminus, pim, pp, sh, gw, ot, s, s_perc, toi_g, sft_g, fo_perc, id")

GoalieBiosRow = namedtuple("GoalieBiosRow", "number, player, team, dob, birthcity, s_p, country, height,weight, c, rk,draft,rnd,ovrl,gp,w, l, ot, gaa, svs, so, id")

SkaterBiosRow = namedtuple("SkaterBiosRow", "number, player, team, pos, dob, birthcity, s_p, country, height, weight, s, draft, rnd, ovrl, rk, gp, g, a, pts, plusminus, pim, toi_g, id")



class PlayerStatsReader(reader.AbstractReader):

    def __init__(self, season, gametype, position, viewname, rowdata):
        self.season = season

        if gametype == "regular":
            self.gametype =  2
        else:
            self.gametype =  3
        self.position = position
        self.viewname = viewname
        self.rowdata = rowdata

    
    def get_row_id(self, row):
        return scraper.get_qp_from_href(row, "id", "/ice/player.htm")


    def readtables(self):

        url = PLAYER_STATS_URL.format(self.season, self.gametype,
                            self.position, self.viewname)

        for page in scraper.get_urls_for_paginated_table(url):
            try: 
                soup = scraper.get_soup (page)
                table = soup.find('table', "stats")
            except:
                logging.warning("Could not read {}".format(page))
                raise StopIteration
            yield table 




def skater_bios_reader(season, gametype):
    return PlayerStatsReader(season, gametype, 
                                    "S", "bios", SkaterBiosRow)

def skater_summary_reader(season, gametype):
    return PlayerStatsReader(season, gametype, 
                                    "S", "summary", SkaterSummaryRow)

def goalie_bios_reader(season, gametype):
    return PlayerStatsReader(season, gametype, 
                                    "G", "goalieBios", GoalieBiosRow)

    