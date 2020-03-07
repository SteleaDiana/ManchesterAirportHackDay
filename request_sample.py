#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:13:53 2020

@author: vladgriguta
"""


url = 'https://opensky-network.org/api/states/all'

import pandas as pd
import requests

data = requests.get(url).json()

cols = ['icao24','callsign','origin_country','time_position','last_contact'
        ,'longitude','latitude','geo_altitude','on_ground','velocity','heading'
        ,'vertical_rate','sensors','baro_altitude','squawk','spi','position_source']

df = pd.DataFrame(data['states'],columns=cols)


import csv, json, sys

fileInput = sys.argv[1]
fileOutput = sys.argv[2]
outputFile = open('csvData.csv', 'w') #load csv file

output = csv.writer(outputFile) #create a csv.write

output.writerow(data[0].keys())  # header row
for row in data:
    output.writerow(row.values()) #values row

