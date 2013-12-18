#!/usr/bin/env 
        

import nhl


reader = nhl.skater_bios_reader("20132014", "regular")

for n, skater in enumerate(reader, 1):
    print n, skater


'''
petfor = nhl.career_reader(8458520, "regular")

for stat in petfor.run():
    print stat.season, stat
'''












