#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""player.py


Example usage:

    p = Player(8471669)

    print p.twitter

    for tbl in p.tables:
        for row in tbl:
            print row

"""

from commons import getdoc
from commons import stringify

PLAYER_CAREER_URL = "http://www.nhl.com/ice/player.htm?id={}"


class Player:
    """Represent an NHL player on nhl.com"""

    def __init__(self, player_id):
        """Loads the player stats page as an ElementTree"""
        url = PLAYER_CAREER_URL.format(player_id)
        self.doc = getdoc(url)

    @property
    def twitter(self):
        """Gets the players twitter handle or None"""
        twitter_tag = self.doc.find(".//a[@class='twitter-follow-button']")
        if twitter_tag is not None:
            return twitter_tag.get("href").split("/")[-1]

    @property
    def tables(self):
        """Grabs all career tables from the player page."""

        playerstats_tables = []

        for table in self.doc.findall(".//table[@class='data playerStats']"):

            headers = [th.text for th in table.findall(".//th")]

            table_group = [headers]

            for row_i in table.findall(".//tr")[1:]:

                data = [stringify(td) for td in row_i.findall("td")]

                table_group.append(data)

            playerstats_tables.append(table_group)

        return playerstats_tables


if __name__ == '__main__':
    p = Player(8471669)

    print(p.twitter)

    for tbl in p.tables:
        for row in tbl:
            print(row)
