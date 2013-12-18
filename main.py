#!/usr/bin/env 
        

from nhl import playerstats


reader = playerstats.skater_bios_reader("20132014", "regular")

for skater in reader.run(42):
    print u"{}({}) : {}".format(skater.player, skater.id, skater.pts)













