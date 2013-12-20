'''
CAREER STATS




'''
import re
import logging

from collections import namedtuple


from nhlreader import getsoup, get_rowdata_as_list, get_qp_from_href


CareerStatsRow = namedtuple("CareerStatsRow", "season, gametype, nhl_team, nhl_id, data")

PLAYER_URL = "http://www.nhl.com/ice/player.htm?id={}"

TABLE_MAP = {
    'regular' : {
        'skater' : namedtuple("SkaterRegular", "season, team, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc"),
        'goalie' : namedtuple("GoalieRegular", "season, team, gp, w, l, t, ot, so, ga, sa, svs, gaa, min")
    },
    'playoff' : {
        'skater' : namedtuple("SkaterPlayoff", "season, team, gp, g, a, p, plusminus, pim, ppg, shg, gwg, s, s_perc"),
        'goalie' : namedtuple("GoaliePlayoff", "season, team, gp, w, l, so, ga, sa, svs, gaa, min")    
    }
}


class CareerStatsTable(object):
    

    def __init__(self, nhl_id, gametype="regular"):
        self.nhl_id = nhl_id
        self.url = PLAYER_URL.format(nhl_id)        
        self.gametype = gametype

        self.datamap = None


    def update_datamap(self, soup):

        is_goalie = soup.find(id="tombstone").find(text=re.compile("Goalie"))

        if is_goalie:
            self.datamap = TABLE_MAP[self.gametype]["goalie"]
        else:
            self.datamap = TABLE_MAP[self.gametype]["skater"]



    def load(self):
        '''Loads the table and updates the datamap'''

        soup = getsoup(self.url)

        self.update_datamap(soup)

        CAREER_TABLES = {
            'regular' : "CAREER REGULAR SEASON STATISTICS",
            'playoff' :  "CAREER PLAYOFF STATISTICS"
        }

        h3 = soup.find("h3", text=CAREER_TABLES[self.gametype])

        return h3.next_sibling


    def readrows(self):

        table = self.load()

        if table is None:
            raise StopIteration

        for row in table.find_all("tr")[1:-1]:
            team_id = get_qp_from_href(row, "tm", "/ice/playersearch.htm")

            try:
                data = self.datamap._make(get_rowdata_as_list(row))
            except Exception as e:
                logging.error("Failed to parse row {} : {}".format(row, e.message))
                raise StopIteration
            
            yield CareerStatsRow("".join(data.season.split("-")), 
                                    self.gametype, 
                                    team_id, 
                                    self.nhl_id,
                                    data)
if __name__ == '__main__':
    
    for p in CareerStatsTable(8445386, "regular").readrows():
        print p