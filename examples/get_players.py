#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nhl

reader = nhl.reader("20122013", gametype="playoff", report='bios')

print reader.fieldnames

for player in reader:
    print player