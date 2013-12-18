#!/usr/bin/env 
        

import nhl

reader = nhl.skater_bios_reader("20132014", "regular")

for skater in reader.run(7):
    print skater













