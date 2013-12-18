The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 


## Basic Usage

```python
from nhl import playerstats


reader = playerstats.skater_bios_reader("20132014", "regular")

for skater in reader.run(42):
    print u"{}({}) : {}".format(skater.player, skater.id, skater.pts)

```        


## What does it read? 

It reads from the [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary): 

It reads the "Summary" and "Bios" reports. 

It reads "All Skaters" and "Goalies". 


