#!/usr/bin/env python

import sys
import nhl
import csv

def main():

    if (len(sys.argv) != 5):
        exit()

    reader = nhl.playerstats(*sys.argv[1:])        

    writer = csv.writer(sys.stdout)

    def encode_for_cl(v):
        if v:
            return v.encode('utf-8')
        else:
            return v
    
    
    for s in reader:
        writer.writerow([s.season, s.gametype, s.nhl_id] + map(encode_for_cl, s.data._asdict().values()))





if __name__ == '__main__':
    main()










        










