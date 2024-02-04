### Author: Ashlynn Wimer
### Date: 2/2/2024
### About: Script for geocoding closed, open, and converted hospitals.
###        Utilizes a quick wrapper I wrote for ease of geocoding.
import pandas as pd
from GoogleApiBuddy import GoogleApiBuddy

## Get API Key and make ApiHelper object
with open('apikeys.txt', 'r') as f:
    API_KEY = f.readline()
api_helper = GoogleApiBuddy(API_KEY)

## Read in closed hospitals, extract address info
closures = pd.read_excel('../data/raw/hospitals/Closures-Database-for-Web.xlsx')

closures = closures[['Address', 'City', 'State', 'Hospital']].dropna()
closures['HID'] = range(0, len(closures))
closures['HID'] = closures['HID'].apply(lambda x: 'H' + str(x).rjust(3, '0'))

geocoded_closures = api_helper.geocode_addresses(closures, ids='HID')

## Read in normal hopsitals, extract address info
hospitals = pd.read_csv('../data/raw/hospitals/Hospital_General_Information.csv',
                        dtype={'Facility ID':str})\
                        .rename({
                            'Facility ID':'HID',
                            'City/Town':'City'
                        }, axis=1)
hospitals['HID'] = hospitals['HID'].apply(lambda x: 'H' + str(x))
hospitals = hospitals[['HID', 'Address', 'City', 'State']].dropna(thresh=2)
geocoded_hosps = api_helper.geocode_addresses(hospitals, ids='HID')

## Read in REH hospitals, extract address info
reh = pd.read_excel('../data/raw/hospitals/REH-Data-for-Web.xlsx', header=1)
reh['HID'] = range(len(closures), len(reh) + len(closures))
reh['HID'] = reh['HID'].apply(lambda x: 'H' + str(x).rjust(3, '0'))
geocoded_reh = api_helper.geocode_addresses(reh, ids='HID')

## Save

# these might be redundant, so we store them separately for now.
geocoded_reh.to_csv('../data/REHGeocoded.csv', index=False)

# join and save the geocoded hosps
geocoded = pd.concat([geocoded_hosps, geocoded_closures], ignore_index=True)
geocoded.to_csv('../data/HospitalsGeocoded.csv', index=False)
