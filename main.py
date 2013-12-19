#!/usr/bin/env 
        
from nhl import playerstats

reader = playerstats.reader("20122013", "regular", "goalies", "bios")

for p in reader.run(3):
    print p



from nhl import player

peter_forsberg = player.reader(8458520)

for career in peter_forsberg:
    print career











