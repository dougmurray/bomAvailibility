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
import re
# This is needed for SSL Certificate errors.
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

# testPart = 'ADA4898-1YRDZ'
# testPart = 'B1H06-V62B'

def click_part_link(page_source, partnum):
    soup = BeautifulSoup(page_source, "html.parser")
    for button in soup.find_all('a'):
        if button.get_text() == 'CGA3E1X7R1E105K080AC':
            return button.get('href')

filename = sys.argv[1]
df = pandas.read_csv(filename, header=0, delimiter=',')
# Remove rows with NaN in PARTNUM column
df.dropna(subset=['PARTNUM'], inplace=True)

# Assumes the csv file as been cleaned and thus only
# has attributes: 'Qty', 'Parts', 'MANUF', 'PARTNUM', 'Value'
# print(df['PARTNUM'])
# print(df.iloc[0, 3])

# mytd = soup.find("td", {"data-atag": "tr-qtyAvailable"}) # this worked once
for i, element in enumerate(df['PARTNUM']):
    try:
        testPart = element
        url = 'https://www.digikey.com/products/en?keywords='
        url += testPart
        # print(url)
        r = requests.get(url)
        r.encoding
        # This
        clicky = click_part_link(r.text, testPart)
        website_preamble = 'https://www.digikey.com'
        specific_part_url = website_preamble + str(clicky)
        print(specific_part_url)
        new_r = requests.get(specific_part_url)
        new_r.encoding
        page_source = new_r.text
        soup = BeautifulSoup(page_source, 'html.parser') # this works in 'Desktop' view
        digikey_quantity = soup.find("span", {"id": "dkQty"})
        quantity = digikey_quantity.get_text()
        print(testPart, int(re.search(r'/d+', quantity).group()))
        
        # Or that
        # page_source = r.text
        # soup = BeautifulSoup(page_source, 'html.parser') # this works in 'Desktop' view
        # digikey_quantity = soup.find("td", {"class": "tr-qtyAvailable ptable-param"})
        # quantity = digikey_quantity.get_text()
        # print(testPart, int(re.search(r'/d+', quantity).group()))
    except AttributeError:
        print(testPart, 'No Results')
        pass
