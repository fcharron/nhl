#!/usr/bin/env 
        
from nhl import playerstats


reader = playerstats.reader("20132014", "regular", "skaters", "summary")
for s in reader.run(7):
    print s













