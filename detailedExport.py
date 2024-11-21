import time
import re
import json
from urllib.request import urlopen
import requests
import pandas as pd
import pprint

# Perform Query - Paste your API Search Query URL into the searchURL
searchURL = "https://www.loc.gov/collections/chronicling-america/?qs=Los+Angeles+oil&ops=~10%21PHRASE&searchType=advanced&start_date=1890-01-01&end_date=1930-12-31&fo=json"

def get_item_ids(url, items=[], conditional='True'):
    # Check that the query URL is not an item or resource link.
    exclude = ["loc.gov/item","loc.gov/resource"]
    if any(string in url for string in exclude):
        raise NameError('Your URL points directly to an item or '
                        'resource page (you can tell because "item" '
                        'or "resource" is in the URL). Please use '
                        'a search URL instead. For example, instead '
                        'of \"https://www.loc.gov/item/2009581123/\", '
                        'try \"https://www.loc.gov/maps/?q=2009581123\". ')

    # request pages of 100 results at a time
    params = {"fo": "json", "c": 100, "at": "results,pagination"}
    call = requests.get(url, params=params)
    # Check that the API request was successful
    if (call.status_code==200) & ('json' in call.headers.get('content-type')):
        data = call.json()
        results = data['results'][:20] # This limits results to the top 20
        for result in results:
            print(f"result: {result}")
            # Filter out anything that's a collection or web page
            filter_out = ("collection" in result.get("original_format")) \
                    or ("web page" in result.get("original_format")) \
                    or (eval(conditional)==False)
            if not filter_out:
                # Get the link to the item record
                if result.get("id"):
                    item = result.get("id")
                    # Filter out links to Catalog or other platforms
                    if item.startswith("http://www.loc.gov/resource"):
                      resource = item  # Assign item to resource
                      items.append(resource)
                    if item.startswith("http://www.loc.gov/item"):
                      items.append(item)
        # Repeat the loop on the next page, unless we're on the last page.
        if data["pagination"]["next"] is not None:
            next_url = data["pagination"]["next"]
            get_item_ids(next_url, items, conditional)

        return items
    else:
            print('There was a problem. Try running the cell again, or check your searchURL.')

# Generate a list of records found from performing a query and save these Item IDs. (Create ids_list based on items found in the searchURL result)
ids_list = get_item_ids(searchURL, items=[])

# Add 'fo=json' to the end of each row in ids_list (All individual ids from from the ids_list are now listed in JSON format in new_ids)
ids_list_json = []
for id in ids_list:
  if not id.endswith('&fo=json'):
    id += '&fo=json'
  ids_list_json.append(id)
ids = ids_list_json

print('\nSuccess! Your API Search Query found '+str(len(ids_list_json))+' related newspaper pages. Proceed to the next step')