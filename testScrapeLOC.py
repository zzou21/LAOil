'''Test scrape LOC: https://www.loc.gov/collections/chronicling-america/?qs=Los+Angeles+oil%21Los+Angeles&ops=~10%21PHRASE&searchType=advanced&start_date=1890-01-01&end_date=1930-12-31&c=600
'''
import requests, os, pprint, re
import pandas as pd
requestMain = requests.get("https://www.loc.gov/collections/chronicling-america/?qs=Los+Angeles+oil&ops=~10%21PHRASE&searchType=advanced&start_date=1890-01-01&end_date=1930-12-31&c=600&fo=json")
print(requestMain)
requestJson = requestMain.json()
print(requestJson) 