#!/usr/bin/env python

'''
PLAYER CAREER STATS





'''
import re
import logging
import urllib2
import urlparse
from collections import namedtuple

from bs4 import BeautifulSoup


import formatters

class NhlPlayerException(Exception):
    pass


PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"


TEAM_ID_REGEX = re.compile(r"^/ice/playersearch.htm")


GOALIE_CAREER_REGULAR_COLS = 'team_id', 'season', 'team', 'gp', 'w', 'l', 't', 'ot', 'so',  'ga', 'sa', 'svperc', 'gaa', 'min'
GOALIE_CAREER_PLAYOFF_COLS = 'team_id', 'season', 'team', 'gp', 'w', 'l', 'so', 'ga', 'sa', 'svperc', 'gaa','min'
SKATER_CAREER_REGULAR_COLS = 'team_id', 'season', 'team', 'gp', 'g', 'a', 'p','plusminus', 'pim', 'ppg', 'shg', 'gwg', 's', 'sperc'
SKATER_CAREER_PLAYOFF_COLS = SKATER_CAREER_REGULAR_COLS


GoalieCareerRegularStats = namedtuple("GoalieCareerRegularStats", GOALIE_CAREER_REGULAR_COLS)
GoalieCareerPlayoffStats = namedtuple("GoalieCareerPlayoffStats", GOALIE_CAREER_PLAYOFF_COLS)
SkaterCareerRegularStats = namedtuple("SkaterCareerRegularStats",SKATER_CAREER_REGULAR_COLS)
SkaterCareerPlayoffStats = namedtuple("SkaterCareerPlayoffStats",SKATER_CAREER_PLAYOFF_COLS)


ROWBUILDERS = {
    'regular' : {
        'goalie' : GoalieCareerRegularStats, 
        'skater' : SkaterCareerRegularStats
    },
    'playoff' : {
        'goalie' : GoalieCareerPlayoffStats, 
        'skater' : SkaterCareerPlayoffStats
    }
}






class Player(object):
    '''Represent an NHL player on nhl.com'''

    def __init__(self, nhl_id):
        self.nhl_id = nhl_id        
        self.pos = "skater"
        self.soup = None
        self._tombstone = None

    
    def gettable(self, header, rowbuilder):
        '''Loads the tables'''

        if self.soup is None:
            self.load()

        h3 = self.soup.find("h3", text=header)

        table = h3.next_sibling

        rowdata = []    
        for row in table.find_all("tr")[1:-1]:

            anchor_tag = row.find("a", href=TEAM_ID_REGEX)
            if anchor_tag:
                qs = urlparse.urlparse(anchor_tag['href']).query
                team_id = urlparse.parse_qs(qs).get("tm", None)[0]
            else: 
                team_id = None

            data = [team_id] + [td.string for td in row.find_all("td")]

            formatted_data = [formatters.DEFAULT_FORMATTERS[k](v) for k,v in zip(rowbuilder._fields, data)]
           
            rowdata.append(rowbuilder._make(formatted_data))

        return rowdata        


    def load(self):

        url = PLAYER_URL.format(self.nhl_id)

        try:
            html = urllib2.urlopen(url).read()
            self.soup = BeautifulSoup(html, 'lxml')
        except Exception as e:
            raise NhlPlayerException("Could not load {} : {}".format(url,
                                                        e.message))

        self._tombstone = self.soup.find(id="tombstone")            
        if self._tombstone.find(text=re.compile("Goalie")):
            self.pos = "goalie"

        return self


    def playoff_stats(self):
        return self.gettable(re.compile("^CAREER PLAYOFF"), 
                ROWBUILDERS['playoff'][self.pos])


    def regular_stats(self):
        return self.gettable(re.compile("^CAREER REGULAR"), 
                ROWBUILDERS['regular'][self.pos])


    def tombstone(self):
        '''Not yet supported'''
        return self._tombstone


    def twitter(self):
        '''gets the players twitter handle or None'''
        if self.soup is None:
            self.load()

        bio_info = self.soup.find(class_="bioInfo")
        twitter_tag = bio_info.find(class_="twitter-follow-button")
        if twitter_tag is not None:
            return twitter_tag['href'].split("/")[-1]




if __name__ == '__main__':

    nhl_player = Player(8458520)

    print nhl_player.twitter()

    career = nhl_player.regular_stats() + nhl_player.playoff_stats() 

    for stats in career:
        print stats        
    



