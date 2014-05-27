#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''nhlstats.py

A command line tool for readings stats from nhl.com.

Example usage:

nhlstats.py 20132014 -g playoffs


'''

import argparse
import csv
import sys
import nhl


def main():

    parser = argparse.ArgumentParser(description='Read playerstats from nhl.com')
    parser.add_argument('seasons', metavar='Seasons',
                        help='an integer for the accumulator')
    parser.add_argument('-p', '--pos', dest='position',
                        action='store',
                        default="S",
                        choices=('S', 'G', 'D', 'L', 'R', 'C'),
                        help='Player position')
    parser.add_argument('-g', '--gametype', dest='gametype',
                        action='store',
                        default="regular",
                        choices=('regular', 'playoffs'),
                        help='Gametype')
    parser.add_argument('-r', '--report', dest='report',
                        action='store',
                        default="summary",
                        choices=('bios', 'summary'),
                        help='Report')
    args = parser.parse_args()

    q = nhl.Query()
    q.season(args.seasons)
    q.gametype(args.gametype)
    q.position(args.position)
    q.report(args.report)

    writer = csv.writer(sys.stdout)
    for row in q.run():
        writer.writerow(map(lambda x: x.encode('utf-8'), row))


if __name__ == '__main__':
    main()
