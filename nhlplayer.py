#!/usr/bin/env python

import sys
import nhl
import csv

def main():

    if (len(sys.argv) < 2):
        exit("Expected NHL player id from nhl.com")

    player = nhl.Player(sys.argv[1]).load()        

    writer = csv.writer(sys.stdout)

    career = player.regular_stats() + player.playoff_stats()

    for stat in career:
        writer.writerow(stat._asdict().values())


if __name__ == '__main__':
    main()










        










