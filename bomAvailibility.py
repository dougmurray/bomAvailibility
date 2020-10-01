#!/usr/bin/env python3
# coding: utf-8
# bomAvailibility.py
# Imports BOM csv and uses OctopartAPI to check the availibility of the parts.
# Run:  python3 bomAvailibility.py /path/to/file/filename.csv
# Author: Douglass Murray


import sys
import pandas
from requests_html import HTMLSession
# import requests
import json
import time
import os
import ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

octopartAPIKey = '515ffdce74e42367a27b'  # Douglass Murray's account
testPart = 'SN74S74N'

url = 'https://www.digikey.com/products/en?keywords='
url += testPart
print(url)

filename = sys.argv[1]
df = pandas.read_csv(filename, header=0, delimiter=',')
# Remove rows with NaN in PARTNUM column
df.dropna(subset=['PARTNUM'], inplace=True)

# Assumes the csv file as been cleaned and thus only
# has attributes: 'Qty', 'Parts', 'MANUF', 'PARTNUM', 'Value'
print(df['PARTNUM'])

session = HTMLSession()
html_response = session.get(url)
print(html_response.html.find('#tr-qtyAvailable ptable-param', first=True))
container = html_response.html.find("tr-qtyAvailable ptable-param", first=True)
# list = container.find('td')
print(container)
# container = response.html.find('<span>SN74S74N</span>')
# print(list)

# r = requests.get(url)
# r.encoding
# page_source = r.text
# print(page_source)
# finder = page_source.find('</html>')  # '<span>SN74S74N</span>'
# print(finder)

# response = urlopen(url) # stupid python 3
# response = urllib2.urlopen(url)  # python 2
# http_content = http.urlopen(url)
# html_bytes = http_content.read()
# output = html_bytes.decode('utf-8')
# print(response)
# Example from Octopart API documentation
# print mpn's
# for result in response['results']:
    # for item in result['items']:
        # print(item['mpn'])
