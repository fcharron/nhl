#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nhl

reader = nhl.reader("20132014", gametype="regular", report='summary')

print reader.fieldnames()

for player in reader:
    print player