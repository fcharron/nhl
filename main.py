#!/usr/bin/env 
        
from nhl import playerstats
from nhl import player


reader = playerstats.reader("20132014")
for s in reader.run(7):
    print s


petfor = player.reader(8458520)
for s in petfor:
    print s












