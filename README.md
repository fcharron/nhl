PyNHL
=====

A Python module for getting player stats from nhl.com. 

Install using [PIP](https://pypi.python.org/pypi/pip): 
```python
pip install pynhl
```


## Basic Usage

```python
import nhl

reader = nhl.reader("20122013", gametype="playoff", report='bios')

print reader.fieldnames()

for player in reader:
    print player
```        


## What does it read? 

It reads from the [Player Stats](http://www.nhl.com/ice/playerstats.htm?season=20122013&gameType=2&team=&position=S&country=&status=&viewName=summary): 

It reads the "Summary" and "Bios" reports. 

It reads "All Skaters", not goalies stats. 


## The nhl2.csv.py Tool

Useful for just getting a CSV file of players stats.

```
usage: nhl2csv.py [-h] [-p] [--headerrow] -s season [-o OUTFILE]
                  [--report {bios,summary}]
```

