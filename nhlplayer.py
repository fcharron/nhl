#!/usr/bin/env python

import sys
import csv
import argparse


from nhl import player as nhl_player


def main():

    parser = argparse.ArgumentParser(description='Get player career from nhl.com.')
    parser.add_argument(dest='ids', metavar='nhl_id', nargs='+', 
                   help='The NHL ID from nhl.com')
    parser.add_argument("-p", "--playoff", dest="playoff", action="store_true", help="Include playoff season", default=False)
    parser.add_argument("-r", "--regular", dest="regular", action="store_true", help="Include regular season", default=False)
    args = parser.parse_args()


    writer = csv.writer(sys.stdout)


    for nhl_id in args.ids:
        player = nhl_player.get(nhl_id)


        if args.regular:
            for stat in player.regular_stats:
                writer.writerow([nhl_id, 'regular'] + stat._asdict().values())

        if args.playoff:
            for stat in player.playoff_stats:
                writer.writerow([nhl_id, 'playoff'] + stat._asdict().values())


if __name__ == '__main__':
    main()










        










