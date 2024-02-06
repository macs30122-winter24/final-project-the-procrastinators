### Author: Dan Gilles
### Date: 2/5/2024
### Description: This script gets data from the census API and saves it to a csv file.

import requests                
import pandas as pd

# get the census api key (possibly unnecessary??)
with open('../census_key.txt', 'r') as f:
    key = f.read().strip()

# get data from the census api and save to csv
for census_type in ['acs1', 'acs5', 'acsse']:
    counties = pd.DataFrame()
    for year in range(2011, 2023):
        if census_type == 'acsse':
            census_vars = 'K200104_001E,K202301_001E,K202301_005E,K201902_001E'
        else:
            census_vars = 'B01001_001E,B23025_001E,B23025_005E,B19013_001E'
        url = f"https://api.census.gov/data/{year}/acs/{census_type}?\
            get={census_vars}&for=county:*&key={key}"
        r = requests.get(url)
        print(census_type, year, r.status_code)
        if r.status_code != 200:
            continue
        data = r.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df['GeoID'] = df['state'] + df['county']
        df = df.drop(columns=['state', 'county'])
        df['Year'] = year
        counties = pd.concat([counties, df])
    counties = counties.melt(id_vars=['GeoID', 'Year'], \
                             value_vars=census_vars.split(','), \
                                var_name='Variable', value_name='Value')\
                                    .rename(columns={'Value': 'Estimate'})\
                                        .sort_values(by=['GeoID', 'Year'])
    counties.to_csv(f"../data/census_data_{census_type}.csv", index=False)