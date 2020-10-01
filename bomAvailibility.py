#!/usr/bin/env python3
# coding: utf-8
# bomAvailibility.py
# Imports BOM csv and uses OctopartAPI to check the availibility of the parts.
# Run:  python3 bomAvailibility.py /path/to/file/filename.csv
# Author: Douglass Murray

import sys
import pandas
import urllib.request as http
import json
import time
# import os # not used yet

octopartAPIKey = '515ffdce74e42367a27b'  # Douglass Murray's account
testPart = 'SN74S74N'
url = 'http://octopart.com/api/v3/parts/match?'
url += '&queries=[{"mpn":"'
url += testPart
url += '"}]'
url += '&apikey='
url += octopartAPIKey
print(url)

filename = sys.argv[1]
df = pandas.read_csv(filename, header=0, delimiter=',')
# Remove rows with NaN in PARTNUM column
df.dropna(subset=['PARTNUM'], inplace=True)

# Assumes the csv file as been cleaned and thus only
# has attributes: 'Qty', 'Parts', 'MANUF', 'PARTNUM', 'Value'
print(df['PARTNUM'])

octopartData = http.urlopen(url).read()
response = json.loads(octopartData)
# request = http.Request(url, None)  # The assembled request
# response = http.urlopen(request)
# octopartData = response.read()
time.sleep(3) # Need 3 seconds between HTTP inquiries for hobbyest use of Octopart API
# Example from Octopart API documentation
# print mpn's
for result in response['results']:
    for item in result['items']:
        print(item['mpn'])
