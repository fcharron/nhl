PyNHL
=====

A Python module for getting player stats from nhl.com 


# Basic Usage

```python
import nhl

reader = nhl.reader("20122013", view='bios')

for player in reader:
	print player
```        

# The nhl2.csv.py Tool

```
usage: nhl2csv.py [-h] [-p] [--headerrow] -s season [-o OUTFILE]
                  [--report {bios,summary}]
```



# What does it read? 

So far it reads only the Player Stats tables at the following URL: 

http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary

It reads the "Summary" and "Bios" reports. 


