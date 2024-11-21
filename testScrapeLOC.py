'''Test scrape LOC: https://www.loc.gov/collections/chronicling-america/?qs=Los+Angeles+oil%21Los+Angeles&ops=~10%21PHRASE&searchType=advanced&start_date=1890-01-01&end_date=1930-12-31&c=600
'''
import requests, os, pprint, re
import pandas as pd
from bs4 import BeautifulSoup
requestMain = requests.get("https://www.loc.gov/collections/chronicling-america/?qs=Los+Angeles+oil&ops=~10%21PHRASE&searchType=advanced&start_date=1890-01-01&end_date=1930-12-31&fo=json")
print(requestMain)
requestJson = requestMain.json()
print(type(requestJson))
print(type(requestJson["results"]))
print(len(requestJson["results"]))
print(requestJson["pagination"])

# itemCounter = 0
# for item in requestJson.items():
#     itemCounter += 1
# pprint.pprint(requestJson["results"][0])