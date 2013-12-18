The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 


## Basic Usage

```python
import nhl

reader = nhl.skater_bios_reader("20132014", "regular")

for skater in reader.run(42):
    print u"{}({}) : {}".format(skater.player, skater.id, skater.pts)
```        


## Player Stats Bios

To get [player statistics](http://www.nhl.com/ice/playerstats.htm?season=20132014&gameType=2&team=&position=S&country=&status=&viewName=bios#), use ```skater_bios_reader```for skaters and ```goalie_bios_reader```for goalies.  


```
import nhl

reader = nhl.skater_bios_reader("20132014", "regular")

for skater in reader.run(7):
    print skater

``` 
Returns the following:
```
SkaterBiosRow(number=u'40', player=u'Michael Grabner', team=u'NYI', pos=u'R', dob=u"Oct 05 '87", birthcity=u'Villach', s_p=None, country=u'AUT', height=u'72', weight=u'186', s=u'L', draft=u'2006', rnd=u'1', ovrl=u'14', rk=None, gp=u'32', g=u'2', a=u'7', pts=u'9', plusminus=u'-6', pim=u'8', toi_g=u'14:43', id='8473546')
SkaterBiosRow(number=u'12', player=u'Michael Raffl', team=u'PHI', pos=u'L', dob=u"Dec 01 '88", birthcity=u'Villach', s_p=None, country=u'AUT', height=u'72', weight=u'195', s=u'L', draft=None, rnd=None, ovrl=None, rk=u'Y', gp=u'22', g=u'2', a=u'6', pts=u'8', plusminus=u'+1', pim=u'14', toi_g=u'13:08', id='8477290')
SkaterBiosRow(number=u'26', player=u'Thomas Vanek', team=u'BUF, NYI', pos=u'L', dob=u"Jan 19 '84", birthcity=u'Vienna', s_p=None, country=u'AUT', height=u'72', weight=u'217', s=u'R', draft=u'2003', rnd=u'1', ovrl=u'5', rk=None, gp=u'32', g=u'10', a=u'12', pts=u'22', plusminus=u'-4', pim=u'24', toi_g=u'18:56', id='8470598')
SkaterBiosRow(number=u'24', player=u'Dmitry Korobov', team=u'TBL', pos=u'D', dob=u"Mar 12 '89", birthcity=u'Novopolotsk', s_p=None, country=u'BLR', height=u'75', weight=u'230', s=u'L', draft=None, rnd=None, ovrl=None, rk=u'Y', gp=u'1', g=u'0', a=u'0', pts=u'0', plusminus=u'+0', pim=u'0', toi_g=u'13:21', id='8477082')
SkaterBiosRow(number=u'44', player=u'Robyn Regehr', team=u'LAK', pos=u'D', dob=u"Apr 19 '80", birthcity=u'Recife', s_p=None, country=u'BRA', height=u'75', weight=u'222', s=u'L', draft=u'1998', rnd=u'1', ovrl=u'19', rk=None, gp=u'35', g=u'0', a=u'4', pts=u'4', plusminus=u'+8', pim=u'16', toi_g=u'19:34', id='8467344')
SkaterBiosRow(number=u'27', player=u'Craig Adams', team=u'PIT', pos=u'R', dob=u"Apr 26 '77", birthcity=u'Seria', s_p=None, country=u'BRN', height=u'72', weight=u'200', s=u'R', draft=u'1996', rnd=u'9', ovrl=u'223', rk=None, gp=u'35', g=u'3', a=u'2', pts=u'5', plusminus=u'-1', pim=u'29', toi_g=u'12:42', id='8465166')
SkaterBiosRow(number=u'56', player=u'Spencer Abbott', team=u'TOR', pos=u'L', dob=u"Apr 30 '88", birthcity=u'Hamilton', s_p=u'ON', country=u'CAN', height=u'69', weight=u'170', s=u'R', draft=None, rnd=None, ovrl=None, rk=u'Y', gp=u'1', g=u'0', a=u'0', pts=u'0', plusminus=u'-2', pim=u'0', toi_g=u'5:16', id='8476805')
```





## What does it read? 

It reads from the [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary): 

It reads the "Summary" and "Bios" reports. 

It reads "All Skaters" and "Goalies". 


