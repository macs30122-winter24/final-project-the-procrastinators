### Author: Ashlynn Wimer
### Date: 2/2/2024
### About: Script for geocoding closed, open, and REH hospitals datasets.
###        Utilizes a quick wrapper I wrote for ease of geocoding.
import pandas as pd
from GoogleApiBuddy import GoogleApiBuddy

## Get API Key and make ApiHelper object
with open('apikeys.txt', 'r') as f:
    API_KEY = f.readline()
api_helper = GoogleApiBuddy(API_KEY)

## Read in normal hopsitals, extract address info
hospitals = pd.read_csv('../data/raw/hospitals/IME_GME_Comp.csv')
hospitals = hospitals[['HID', 'Address', 'City', 'State']].drop_duplicates('HID').reset_index().drop('index', axis=1)
geocoded_hosps = api_helper.geocode_addresses(hospitals, ids='HID')

geocoded_hosps.to_csv('../data/HospitalsGeocoded.csv')