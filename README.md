The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 

Before you use this, please read the NHL.com [terms of service](http://www.nhl.com/ice/page.htm?id=26389). In essence, you can download content FOR PERSONAL USE ONLY.  


## Getting started

The package is available from [PyPI](https://pypi.python.org/pypi/nhl/2.0), the package index for Python:

```
pip install nhl
```

## Player Stats

To get [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary) for a given season:

```python
from nhl import playerstats

reader = playerstats.reader("20132014")
for s in reader.run(7):
    print s

```        

The following parameters are avilable on ```playerstats.reader``` in order to get different kinds of stats.


* ```season``` - e.g. "20122013"
* ```gametype``` - 'regular' | 'playoff'
* ```position``` - 'skaters' | 'goalies'
* ```report``` - 'summary' | 'bios'


Note that the kinds of stats are different for skaters and goalies.


## Career Stats

The following gets Peter Forsberg's career stats:

```python
from nhl import player

petfor = player.reader(8458520)
for s in petfor:
    print s
```



