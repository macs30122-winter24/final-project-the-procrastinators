### Author: Dan Gilles
### Date: 2/5/2024
### Description: This script gets data from the census API and saves it to a csv file.

import requests                
import pandas as pd

# get the census api key (possibly unnecessary??)
with open('../census_key.txt', 'r') as f:
    key = f.read().strip()

# get data from the census api and save to csv
meanings = ['Total Population', 'Labor Force', 'Unemployed', 'Median Income']
census_types = ['acs1', 'acs5', 'acsse']
census_vars = {'acs1': 'B01001_001E,B23025_001E,B23025_005E,B19013_001E', \
    'acs5': 'B01001_001E,B23025_001E,B23025_005E,B19013_001E', \
    'acsse': 'K200104_001E,K202301_001E,K202301_005E,K201902_001E'}

for census_type in census_types:
    counties = pd.DataFrame()
    vars = census_vars[census_type]
    for year in range(2011, 2023):
        url = f"https://api.census.gov/data/{year}/acs/{census_type}?get={vars}&for=county:*&key={key}"
        r = requests.get(url)
        print(census_type, year, r.status_code)
        if r.status_code != 200:
            continue
        data = r.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df['GEOID'] = df['state'] + df['county']
        df = df.drop(columns=['state', 'county'])
        df['Year'] = year
        counties = pd.concat([counties, df])
    counties.rename(columns=dict(zip(vars.split(','), meanings)), inplace=True)
    counties = counties[['Year', 'GEOID'] + meanings]
    display(counties)
    counties.to_csv(f"../data/census_data_{census_type}.csv", index=False)