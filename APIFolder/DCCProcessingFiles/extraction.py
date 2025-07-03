import re
import json
from urllib.request import urlopen
import requests
import pandas as pd
import pprint

# Test to get all search results:
searchURLTest = "https://www.loc.gov/collections/chronicling-america/?end_date=1930-12-31&ops=~10!PHRASE&qs=Los+Angeles+oil!Los+Angeles&searchType=advanced&sp=1&start_date=1890-01-01&fo=json"

def get_item_ids_test(url, items=[], conditional='True'):
    global numberOfResults
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
        results = data['results'] # deleted the top 20 limit
        for result in results:
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
            print(f"Total number of pages: {data['pagination']['total']}")
            get_item_ids_test(next_url, items, conditional)

        return items
    else:
            print('There was a problem. Try running the cell again, or check your searchURL.')

# Generate a list of records found from performing a query and save these Item IDs. (Create ids_list based on items found in the searchURL result)
ids_list_test = get_item_ids_test(searchURLTest, items=[])

# Add 'fo=json' to the end of each row in ids_list (All individual ids from from the ids_list are now listed in JSON format in new_ids)
ids_list_json_test = []
for id in ids_list_test:
  if not id.endswith('&fo=json'):
    id += '&fo=json'
  ids_list_json_test.append(id)
ids = ids_list_json_test

print('\nSuccess! Your API Search Query found '+str(len(ids_list_json_test))+' related newspaper pages. Proceed to the next step')

# Create a list of dictionaries to store the item metadata
item_metadata_list = []

counter = 0
# Iterate over the list of item IDs
for item_id in ids_list_json_test:
  item_response = requests.get(item_id)

  # Check if the API call was successful and Parse the JSON response
  if item_response.status_code == 200:
    # Iterate over the ids_list_json list and extract the relevant metadata from each dictionary.
    item_data = item_response.json()
    # NOT filtering out newspapers that do not have a city associated with it.
    # if 'location_city' not in item_data['item']:
    #   continue

    # Extract the relevant item metadata
    Newspaper_Title = item_data['item']['newspaper_title']
    Issue_Date = item_data['item']['date']
    Page = item_data['pagination']['current']
    State = item_data['item']['location_state']
    try:
       City = item_data['item']['location_city']
    except KeyError:
       pass
    LCCN = item_data['item']['number_lccn']
    Contributor = item_data['item']['contributor_names']
    Batch = item_data['item']['batch']
    pdf = item_data['resource']['pdf']

    # Add the item metadata to the list
    item_metadata_list.append({
        'Newspaper Title': Newspaper_Title,
        'Issue Date': Issue_Date,
        'Page Number': Page,
        'LCCN': LCCN,
        'City': City,
        'State': State,
        'Contributor': Contributor,
        'Batch': Batch,
        'PDF Link': pdf,
    })
    counter += 1
    print(f"Processed {counter} results.")
    

# Change date format to MM-DD-YYYY
for item in item_metadata_list:
  item['Issue Date'] = pd.to_datetime(item['Issue Date']).strftime('%m-%d-%Y')

# Create a Pandas DataFrame from the list of dictionaries
df = pd.DataFrame(item_metadata_list)

print('\nSuccess! Ready to proceed to the next step!')

# Add your Local saveTo Location (e.g. C:/Downloads/)
saveTo = '/hpc/home/zz341/test4'

# Set File Name. Make sure to rename the file so it doesn't overwrite previous!
filename = 'LOCLAOilInitialExtractBlanketCities'

metadata_dataframe = pd.DataFrame(item_metadata_list)
metadata_dataframe.to_csv(saveTo + '/' + filename + '.csv')
print("Finished compiling CSV")
metadata_dataframe