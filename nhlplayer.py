#!/usr/bin/env python

import sys
import nhl
import csv

def main():

    if (len(sys.argv) < 2):
        exit("Expected NHL player id from nhl.com")

    player = nhl.player(sys.argv[1])        

    writer = csv.writer(sys.stdout)

    for s in player.career():
        writer.writerow(s._asdict().values())




if __name__ == '__main__':
    main()










        










