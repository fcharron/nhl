#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''nhlstats.py

A command line tool for readings stats from nhl.com.


'''

import csv
import sys
import nhl


writer = csv.writer(sys.stdout)


def writerow(row):
    writer.writerow(map(lambda x: x.encode('utf-8'), row))


def main():

    args_len = len(sys.argv)

    if args_len == 3 and sys.argv[1] == "player":

        player_id = sys.argv[2]

        for tbl in nhl.Player(player_id).tables:
            for row in tbl:
                writerow(row)
    else:
        q = nhl.Query()

        q.season("20132014").playoffs().position("S").summary()

        for row in q.run():
            writerow(row)


if __name__ == '__main__':
    main()
