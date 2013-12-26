#!/usr/bin/env python

'''
PLAYER CAREER STATS





'''
import re
import urllib2
from collections import namedtuple

from bs4 import BeautifulSoup

import formatters

DATA_MAP = {
    'integers' : ('gp', 'g', 'a', 'p', 'pts', 'plusminus', 'pim', 'pp', 'sh', 'gw', 'gt', 'ot', 'nhl_id', 'number', 'ppg', 'shg', 'gwg', 'gs', 'ga', 'sv', 'l', 'w', 't', 'sa', 'so', 'ht', 'wt', 'draft', 'rnd', 'ovrl'),
    'floats' : ('sperc', 'foperc', 'gaa', 'svperc', 'sftg'),
    'minutes' : ('toig', 'toi', 'min')
}
formatter = formatters.Formatter(DATA_MAP)


class NhlPlayerException(Exception):
    pass


PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"


class StatsTable(object):

    TEAM_ID_REGEX = re.compile(r"^/ice/playersearch.htm")


    def __init__(self, page):
        h3 = page.find("h3", text=re.compile("^CAREER {}".format(self.gametype).upper()))
        self.table = h3.next_sibling


    def make_rowdataclass(self):
        '''Returns a namedtuple class with the table's column names, plus gametype and team ID'''
        column_names = [th.string.lower().replace("+/-","plusminus").replace("%","perc") for th in self.table.find("tr").find_all("th")]

        return namedtuple("CareerStats", column_names)


    def readrows(self):

        rowdataclass = self.make_rowdataclass()

        for row in self.table.find_all("tr")[1:-1]:

            data = [td.string for td in row.find_all("td")]

            formatted_data = [formatter.format(k, v) for k,v in zip(rowdataclass._fields, data)]

            yield rowdataclass._make(formatted_data)


    def __iter__(self):
        return self.readrows()




class RegularStatsTable(StatsTable):
    gametype = "REGULAR"

class PlayoffStatsTable(StatsTable):
    gametype = "PLAYOFF"



class Tombstone(object):
    def __init__(self, page):
        self.tombstone = page.find(id="tombstone")


    def position(self):
        if self.tombstone.find(text=re.compile("Goalie")):
            return "goalie"



class Twitter(object):
    def __init__(self, page):
        self.handle = None
        bio_info = page.find(class_="bioInfo")
        twitter_tag = bio_info.find(class_="twitter-follow-button")
        if twitter_tag is not None:
            self.handle = twitter_tag['href'].split("/")[-1]



class PlayerPage(object):
    '''Represent an NHL player on nhl.com'''

    def __init__(self, soup):
        self.soup = soup

    @property
    def regular_stats(self):
        return RegularStatsTable(self.soup)

    @property
    def playoff_stats(self):
        return PlayoffStatsTable(self.soup)

    @property
    def tombstone(self):
        '''Not yet supported'''
        return Tombstone(self.soup)

    @property
    def twitter(self):
        '''gets the players twitter handle or None'''
        return Twitter(self.soup)



def get(nhl_id):
    url = PLAYER_URL.format(nhl_id)
    try:
        html = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html, 'lxml')
    except Exception as e:
        raise NhlPlayerException("Could not load {} : {}".format(url,
                                                    e.message))

    return PlayerPage(soup)



if __name__ == '__main__':

    import itertools 

    nhl_player = get(8458520)

    for stats in itertools.chain(nhl_player.regular_stats, nhl_player.playoff_stats):
        print stats        



