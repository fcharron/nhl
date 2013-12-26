#!/usr/bin/env python

import sys
import nhl
import csv
import argparse


def main():

    parser = argparse.ArgumentParser(description='Get player stats from nhl.com.')
    parser.add_argument("-s", "--season", dest="season", action="store", help="Season, e.g. 20122013", required="True")
    parser.add_argument("-r", "--report", dest="report", action="store", help="The report, see nhl.com/ice", choices="('bios', 'summary')", default="bios")
    parser.add_argument("-p", "--position", dest="position", action="store", help="Position", choices=('skaters', 'goalies'), default="skaters")
    parser.add_argument("-g", "--gametype", dest="gametype", action="store", help="Gametype", choices=('regular', 'playoff'), default="regular")

    args = parser.parse_args()


    q = nhl.playerstats.Query()
    q.report(args.report)
    q.season(args.season)
    q.position(args.position)
    q.gametype(args.gametype)


    writer = csv.writer(sys.stdout)
    
    
    for s in q.run():
        writer.writerow(map(lambda s:s.encode('utf-8') if isinstance(s,unicode) else s, 
                                            s._asdict().values()))



if __name__ == '__main__':
    main()










        










