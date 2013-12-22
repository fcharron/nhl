#!/usr/bin/env python

import sys
import nhl
import csv

def main():

    if (len(sys.argv) < 2):
        exit("Expected NHL player id from nhl.com")

    player = nhl.Player(sys.argv[1]).load()        

    writer = csv.writer(sys.stdout)

    for c in ('regular', 'playoff'):
    	for stat in player.stats(c):
        	writer.writerow(stat._asdict().values())



if __name__ == '__main__':
    main()










        










