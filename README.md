The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 

Version 3.1 uses [lxml](http://lxml.de) for parsing which is much faster than the previously used BeautifulSoup library.

Before you use this, please read the NHL.com [terms of service](http://www.nhl.com/ice/page.htm?id=26389). In essence, you can download content FOR PERSONAL USE ONLY.  


## Getting started

The package is available from [PyPI](https://pypi.python.org/pypi/nhl), the package index for Python:

```
pip install nhl
```


## As a Command Line Tool

To print out NHL stats to the commands line, use the command line tool ```nhlstats.py```. For example:

```
python nhlstats.py 20132014 --gametype=playoffs
```

Produces the following result:

```
nhl_id,number,Player,Team,Pos,GP,G,A,P,+/-,PIM,PPG,PPP,SHG,SHP,GW,OT,S,S%,TOI/G,Sft/G,FO%
8471685,1,Anze Kopitar,LAK,C,18,5,17,22,+8,12,1,6,0,0,1,0,30,16.7,19:47,25.4,55.4
8470604,2,Jeff Carter,LAK,C,18,8,12,20,+6,2,4,7,0,0,0,0,44,18.2,16:47,23.5,46.7
8468483,3,Marian Gaborik,LAK,R,18,10,6,16,+3,4,2,6,0,0,1,1,53,18.9,16:37,21.4,0.0
8468508,4,Justin Williams,LAK,R,18,6,9,15,+8,31,2,3,0,0,1,0,40,15.0,15:47,21.1,66.7
8470612,5,Ryan Getzlaf,ANA,C,12,4,11,15,-2,10,1,6,0,1,0,0,32,12.5,21:25,27.3,39.4
8473604,6,Jonathan Toews,CHI,C,16,8,6,14,+5,6,1,2,1,1,4,1,27,29.6,21:30,31.1,55.2
```


## Playerstats

To get [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary) for a given season:

```python
import nhl 

q = nhl.Query()
q.season("20132014")
q.gametype("regular")
q.position("G")
q.report("bios")

for row in q.run():
    print row

```        

The following parameters can be set on ```Query()``` in order to get different kinds of stats.

* ```season()``` - e.g. "20122013"
* ```gametype()``` - regular stats
* ```position()``` - 'G' | 'S' | 'F'
* ```report()``` - summary or bios
* ```team()``` - 3-letter team name, e.g. ANA


Note that the kinds of stats are different for skaters and goalies.


## Player

To get the stats tables for a specific player, you must know the player's NHL ID. Get the player's page with ```Player()``` and the tables are available in a list as ```tables```.

```python
player = Player(8471685)

print player.twitter

for row in player.tables[0]:
    print row

```



