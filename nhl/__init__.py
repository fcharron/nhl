from careerstats import CareerStatsTable
from playerstats import PlayerStatsTable



class NhlException(Exception):
    pass



class TableReader(object): 

    def __init__(self, table):
        self.table = table


    def run(self, limit=None):
        '''Returns one row at the time'''        
        row_counter = 0
        for row in self.table.readrows():
            if row_counter == limit:
                raise StopIteration

            yield row            
            row_counter += 1

    
    def fetch(self, limit=None):
        '''Returns all table rows as one (potentially empty or very long) list
        '''
        return list(self.run(limit))

    
    def __iter__(self):
        return self.run()



def careerstats(nhl_id, gametype="regular"):
    return TableReader(CareerStatsTable(nhl_id, gametype))


def playerstats(season, gametype="regular", position="skaters", report="bios"):

    if gametype not in ('regular', 'playoff') or position not in ('skaters', 'goalies') or report not in ('bios', 'summary'):
        return None

    playerstatstable = PlayerStatsTable(season, gametype, position, report)
    return TableReader(playerstatstable)


if __name__ == '__main__':

    for p in careerstats(8445386, "regular").run(5):
        print p


    for s in playerstats("20132014", "regular", "skaters", "bios").run(7):
        print s
