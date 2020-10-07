import os
import ssl
import requests
from bs4 import BeautifulSoup

# This is needed for SSL Certificate errors.
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.digikey.com/products/en?keywords=CGA3E1X7R1E105K080AC'    

def click_part_link(page_source):
    soup = BeautifulSoup(page_source, "html.parser")
    for button in soup.find_all('a'):
        if button.get_text() == 'CGA3E1X7R1E105K080AC':
            return button.get('href')

r = requests.get(url)
# r.encoding
# print(r.text)
clicky = click_part_link(r.text)
print('https://www.digikey.com' + str(clicky))
# https://www.digikey.com/en/products/detail/tdk-corporation/CGA3E1X7R1E105K080AC/2672824
