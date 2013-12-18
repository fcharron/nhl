The Python NHL Reader
======================

A Python module for getting player stats from nhl.com. 


## Basic Usage

```python
from nhl import playerstats


reader = playerstats.reader("20132014", "regular", "skaters", "summary")
for s in reader.run(7):
    print s
```        

Returns:
```
SkaterSummary(number=u'1', player=u'Sidney Crosby', team=u'PIT', pos=u'C', gp=u'35', g=u'19', a=u'28', pts=u'47', plusminus=u'+4', pim=u'20', pp=u'6', sh=u'0', gw=u'4', ot=u'1', s=u'117', s_perc=u'16.2', toi_g=u'22:14', sft_g=u'23.9', fo_perc=u'51.2', id='8471675')
SkaterSummary(number=u'2', player=u'Patrick Kane', team=u'CHI', pos=u'R', gp=u'37', g=u'20', a=u'26', pts=u'46', plusminus=u'+6', pim=u'12', pp=u'9', sh=u'0', gw=u'6', ot=u'0', s=u'121', s_perc=u'16.5', toi_g=u'19:47', sft_g=u'22.9', fo_perc=u'33.3', id='8474141')
SkaterSummary(number=u'3', player=u'Evgeni Malkin', team=u'PIT', pos=u'C', gp=u'32', g=u'9', a=u'32', pts=u'41', plusminus=u'+2', pim=u'32', pp=u'3', sh=u'0', gw=u'2', ot=u'0', s=u'92', s_perc=u'9.8', toi_g=u'19:42', sft_g=u'21.2', fo_perc=u'51.9', id='8471215')
SkaterSummary(number=u'4', player=u'Ryan Getzlaf', team=u'ANA', pos=u'C', gp=u'33', g=u'16', a=u'23', pts=u'39', plusminus=u'+15', pim=u'15', pp=u'4', sh=u'0', gw=u'6', ot=u'1', s=u'84', s_perc=u'19.0', toi_g=u'20:47', sft_g=u'25.0', fo_perc=u'49.1', id='8470612')
SkaterSummary(number=u'5', player=u'Alex Ovechkin', team=u'WSH', pos=u'L', gp=u'32', g=u'28', a=u'10', pts=u'38', plusminus=u'-12', pim=u'22', pp=u'12', sh=u'0', gw=u'4', ot=u'2', s=u'168', s_perc=u'16.7', toi_g=u'21:24', sft_g=u'21.8', fo_perc=u'100.0', id='8471214')
SkaterSummary(number=u'6', player=u'John Tavares', team=u'NYI', pos=u'C', gp=u'35', g=u'13', a=u'25', pts=u'38', plusminus=u'-7', pim=u'30', pp=u'3', sh=u'0', gw=u'2', ot=u'0', s=u'105', s_perc=u'12.4', toi_g=u'20:43', sft_g=u'22.1', fo_perc=u'48.3', id='8475166')
SkaterSummary(number=u'7', player=u'Corey Perry', team=u'ANA', pos=u'R', gp=u'36', g=u'22', a=u'15', pts=u'37', plusminus=u'+15', pim=u'32', pp=u'4', sh=u'0', gw=u'7', ot=u'0', s=u'132', s_perc=u'16.7', toi_g=u'19:52', sft_g=u'23.8', fo_perc=u'41.7', id='8470621')
```


## What does it read? 

The following tables can be read from [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary): 


* Regular and Playoff
* Summary and Bios reports
* All Skaters or All Goalies


