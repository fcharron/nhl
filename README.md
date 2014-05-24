The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 

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
q.report("bios")

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


## Career Stats

TBD



