The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 

Version 3.0 uses [lxml](http://lxml.de) for parsing which is much faster than the previously used BeautifulSoup library. 

Before you use this, please read the NHL.com [terms of service](http://www.nhl.com/ice/page.htm?id=26389). In essence, you can download content FOR PERSONAL USE ONLY.  


## Getting started

The package is available from [PyPI](https://pypi.python.org/pypi/nhl), the package index for Python:

```
pip install nhl
```

## Player Stats

To get [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary) for a given season:

```python
import nhl 

q = nhl.Query()
q.season("20132014")
q.regular()
q.position("G")
q.bios()

for row in q.run():
    print row

```        

The following parameters can be set on ```Query()``` in order to get different kinds of stats.

* ```season()``` - e.g. "20122013"
* ```regular()``` - regular stats
* ```playoffs()``` - playoff stats
* ```position()``` - 'G' | 'S' | 'F'
* ```summary()``` - summary report
* ```bios()``` - bios report


Note that the kinds of stats are different for skaters and goalies.


## Player

To get the stats tables for a specific player, you must know the player's NHL ID. Get the player's page with ```Player()``` and the tables are available in a list as ```tables```.

```python
 player = Player(8471685)

    print player.twitter

    for row in player.tables[0]:
        print row

```



