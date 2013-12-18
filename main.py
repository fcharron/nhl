#!/usr/bin/env 
        

import nhl

'''
reader = nhl.skater_bios_reader("20132014", "regular")

for skater in reader.run(7):
    print skater
'''

petfor = nhl.career_reader(8458520, "regular")

for stat in petfor.run():
    print stat.season, stat













