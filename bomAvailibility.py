#!/usr/bin/env python3
# coding: utf-8
# bomAvailibility.py
# Imports BOM csv and uses OctopartAPI to check the availibility of the parts.
# Run:  python3 bomAvailibility.py /path/to/file/filename.csv
# Author: Douglass Murray

import os
import ssl
import sys
import pandas
import requests
from bs4 import BeautifulSoup
# This is needed for SSL Certificate errors.
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

# testPart = 'ADA4898-1YRDZ'
# testPart = 'B1H06-V62B'

filename = sys.argv[1]
df = pandas.read_csv(filename, header=0, delimiter=',')
# Remove rows with NaN in PARTNUM column
df.dropna(subset=['PARTNUM'], inplace=True)

# Assumes the csv file as been cleaned and thus only
# has attributes: 'Qty', 'Parts', 'MANUF', 'PARTNUM', 'Value'
print(df['PARTNUM'])
print(df.iloc[0, 3])

# mytd = soup.find("td", {"data-atag": "tr-qtyAvailable"}) # this worked once
for i, element in enumerate(df['PARTNUM']):
    try:
        testPart = element
        url = 'https://www.digikey.com/products/en?keywords='
        url += testPart
        # print(url)
        r = requests.get(url)
        r.encoding
        page_source = r.text
        soup = BeautifulSoup(page_source, 'html.parser') # this works in 'Desktop' view
        digikey_quantity = soup.find("td", {"class": "tr-qtyAvailable ptable-param"})
        quantity = digikey_quantity.get_text()
        pretty_quantity = quantity.strip()
        print(testPart, pretty_quantity)
    except AttributeError:
        print(testPart, 'No Results')
        pass
