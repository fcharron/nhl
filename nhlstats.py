#!/usr/bin/env python

import sys
import nhl
import csv

def main():


    pstats = nhl.PlayerStats()

    pstats.season(sys.argv[1])

    writer = csv.writer(sys.stdout)

    def encode_for_cl(v):
        if v:
            return v.encode('utf-8')
        else:
            return v
    
    
    for s in pstats:
        writer.writerow(s._asdict().values())



if __name__ == '__main__':
    main()










        










