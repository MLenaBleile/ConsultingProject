import json
import codecs
import requests
import pandas as pd
from pandas.io.json import json_normalize

def get_county_spending(counties=None):
    if counties == None:
        payload=   {
          "filter": {
              "def_codes": ["L", "M", "N", "O", "P", "U"]
          },
          "geo_layer": "county",
          #"geo_layer_filters":,
          "scope": "recipient_location",
          "spending_type": "obligation"
      }
    else:
        payload=   {
          "filter": {
              "def_codes": ["L", "M", "N", "O", "P", "U"]
          },
          "geo_layer": "county",
          "geo_layer_filters": counties,
          "scope": "recipient_location",
          "spending_type": "obligation"
      }

    r = requests.post('https://api.usaspending.gov/api/v2/disaster/spending_by_geography/', json=payload)

    # json flatten unnecessary but allows the for loop to functionwith indices in current implementation
    # can't use json_read from pd due to nested json
    county_json = json_normalize(r.json())
    init_data = county_json['results'][0]
    county_spending = pd.DataFrame(data=init_data)

    for i in range(len(county_json)):
        county_spending[i] = county_json['results'][i]
    # handle json_normalize artifact
    county_spending = county_spending.drop(columns=0)
    
    return county_spending