'''
PLAYER CAREER STATS





'''
import re
import logging
import urllib2
import urlparse
from collections import namedtuple

from bs4 import BeautifulSoup

from tablereader import TableReader


def str_(s): 
    if s: return unicode(s.strip())

def float_(s): 
    try:
        return float(s)
    except:
        return None

def int_(s): 
    try:
        return int(s)
    except:
        return None


def min_(s):
    if s:
        if "," in s:
            t, h = s.split(",")
            return 1000*int(t)+int(h)
        else:
            return int(s)    

'''

'''
class GoalieCareerRegularStats(namedtuple("GoalieCareerRegularStats", 
    "gametype, season, team_id, team_name, gp, w, l, t, ot, so,  ga, sa, svs, gaa, min")):
    
    @classmethod
    def _fromrowdata(cls, gametype, team_id, data):
        return cls(
            gametype = gametype,
            season = "".join(data[0].strip().split("-")),
            team_id = team_id,
            team_name = data[1].strip(),
            gp = int_(data[2]),
            w = int_(data[3]),
            l = int_(data[4]),
            t = int_(data[5]),
            ot = int_(data[6]),
            so = int_(data[7]),
            ga = int_(data[8]),
            sa = int_(data[9]),
            svs = float_(data[10]),
            gaa = float_(data[11]),
            min = min_(data[12])
            )


class GoalieCareerPlayoffStats(namedtuple("GoalieCareerPlayoffStats", 
    "gametype, season, team_id, team_name, gp, w, l, so, ga, sa, svs, gaa, min")):
    
    @classmethod
    def _fromrowdata(cls, gametype, team_id, data):
        return cls(
            gametype = gametype,
            season = "".join(data[0].strip().split("-")),
            team_id = team_id,
            team_name = data[1].strip(),            
            gp = int_(data[2]),
            w = int_(data[3]),
            l = int_(data[4]),
            so = int_(data[5]),
            ga = int_(data[6]),
            sa = int_(data[7]),
            svs = float_(data[8]),
            gaa = float_(data[9]),
            min = min_(data[10])
            )


class SkaterCareerStats(namedtuple("SkaterCareerStats", 
    "gametype, season, team_id, team_name, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc")):
  
    @classmethod
    def _fromrowdata(cls, gametype, team_id,  data):
        return cls(
            gametype = gametype,
            season = "".join(data[0].strip().split("-")),
            team_id = team_id,
            team_name = str_(data[1]),
            gp = int_(data[2]),
            g = int_(data[3]), 
            a = int_(data[4]),
            p = int_(data[5]),
            plusminus = int_(data[6]),
            pim = int_(data[7]),
            ppg = int_(data[8]),
            shg = int_(data[9]),
            gwg = int_(data[10]),
            s = int_(data[11]),
            s_perc = float_(data[12])
            )
                



PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"

TABLE_MAP = {
    'regular' : ("CAREER REGULAR SEASON STATISTICS", {'goalie' : GoalieCareerRegularStats, 'skater' : SkaterCareerStats}),
    'playoff' : ("CAREER PLAYOFF STATISTICS", {'goalie' : GoalieCareerPlayoffStats, 'skater' : SkaterCareerStats})
}

TEAM_ID_REGEX = re.compile(r"^/ice/playersearch.htm")

class CareerStats(object):
    
    def __init__(self, soup):
        self.soup = soup 

        if self.soup.find(id="tombstone").find(text=re.compile("Goalie")):
            self.pos = "goalie"
        else:
            self.pos = "skater"
       

    def readtables(self):
        '''Loads the tables'''

        for gametype in TABLE_MAP.keys():
            h3 = self.soup.find("h3", text=TABLE_MAP[gametype][0])
            yield (gametype, h3.next_sibling)


    def readrows(self):

        for gametype, table in self.readtables():

            datamapper = TABLE_MAP[gametype][1][self.pos]

            for row in table.find_all("tr")[1:-1]:

                try:
                    
                    anchor_tag = row.find("a", href=TEAM_ID_REGEX)
                    if anchor_tag:
                        qs = urlparse.urlparse(anchor_tag['href']).query
                        team_id = urlparse.parse_qs(qs).get("tm", None)[0]
                    else: 
                        team_id = None

                    data = [td.string for td in row.find_all("td")]
                except Exception as e:
                    logging.error("Failed to parse row {} : {}".format(row, 
                                                                    e.message))
                    raise StopIteration
                
                yield datamapper._fromrowdata(gametype, team_id, data)



class Player(object):
    '''Represent an NHL player on nhl.com'''

    def __init__(self, nhl_id):
        url = PLAYER_URL.format(nhl_id)
        html = urllib2.urlopen(url).read()
        self.soup = BeautifulSoup(html, 'lxml')


    def career(self):
        '''Returns a TableReader for reading all career stats rows'''
        return TableReader(CareerStats(self.soup))


    def tombstone(self):
        '''Not yet supported'''
        return self.soup.find(id="tombstone")


    def twitter(self):
        '''gets the players twitter handle or None'''
        bio_info = self.soup.find(class_="bioInfo")
        twitter_tag = bio_info.find(class_="twitter-follow-button")
        if twitter_tag is not None:
            return twitter_tag['href'].split("/")[-1]



def player(nhl_id):
    return Player(nhl_id)


if __name__ == '__main__':

    nhl_player = player(8458520)
    print nhl_player.twitter()


    for stats in nhl_player.career():
        print stats        
    
    