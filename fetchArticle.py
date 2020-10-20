from googlesearch import search
import requests
from bs4 import BeautifulSoup
'''
query="Reliance Fraud"
for url in search(query,        # The query you want to run
                tld = 'com',  # The top level domain
                lang = 'en',  # The language
                num = 10,     # Number of results per page
                start = 1,    # First result to retrieve
                stop = 3,  # Last result to retrieve
                pause = 2.0,  # Lapse between HTTP request
               ):
    print(url)
    '''
url="https://economictimes.indiatimes.com/markets/stocks/news/future-enterprises-defaults-on-interest-payments-of-ncds/articleshow/78392099.cms"
html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'html.parser')
print(soup.get_text())
