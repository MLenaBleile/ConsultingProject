import json
import codecs
import requests
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np

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

# Fix this mess. Use joins.
# Crazy slow

def spend_county_state_map(spend, ACS, covid):
    val_count = spend['county_name'].value_counts()
    dupes = [i for i in val_count.index if val_count[i]!=1]
    spend['State'] = ''
    for idx in spend.index:
        if spend.loc[idx, 'county_name'] in dupes:
            # Get a subset of the ACS data that matches entry county name
            ACS_sub = ACS[ACS['county_name']==spend.loc[idx, 'county_name']][['id','county_name','tot','State']]
            # calculate the difference between spend entry and ACS populations
            ACS_sub['diffs'] = np.abs(spend.loc[idx, 'population']-ACS_sub['tot'])
            # assign the lowest difference to the spending df
            try:
                spend.loc[idx,'State']= ACS_sub[ACS_sub['diffs']==min(ACS_sub['diffs'])]['State'].values[0]
            except:
                spend.loc[idx,'State']= 'Missing'
                
            # Current implementation allows for multiple entries of the same county into different records
            # in the spending df which is impossible. Consider implementing a low pass filter with the
            # alternative case being unknown or a counter for number of assignments
            
        else:
            val = spend['county_name'][idx]
            #print(val)
            #print(covid[covid['county_name']==val].State.values[0])
            #print(spend.head())
            try:
                spend.loc[idx, 'State'] = covid[covid['county_name']==val].State.values[0]
            except:
                spend.loc[idx, 'State'] = 'Missing'
    
    return spend


# https://gist.github.com/rogerallen/1583593

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# thank you to @kinghelix and @trevormarburger for this idea
abbrev_us_state = dict(map(reversed, us_state_abbrev.items()))


        