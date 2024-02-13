### Author: Dan Gilles
### Date: 2/13/2024
### Description: This script gets the data from the IRS, Census Bureau and
### Rurality and merges it into two files, a full dataset with all data and a 
### smaller dataset with only counties having data from every survey.

import pandas as pd

meanings = ['Total Population', 'Labor Force', 'Unemployed', 'Median Income']
census_types = ['acs1', 'acs5', 'acsse']
data = pd.read_csv("../data/irs_data.csv")
data_full = pd.read_csv("../data/irs_data.csv")

for census_type in census_types:
    counties = pd.read_csv(f"../data/census_data_{census_type}.csv")
    meanings2 = [m + ' (' + census_type.upper() + ')' for m in meanings]
    counties.rename(columns=dict(zip(meanings, meanings2)), inplace=True)
    data = pd.merge(data, counties, on=['Year', 'GEOID'], how='inner')
    data_full = pd.merge(data_full, counties, on=['Year', 'GEOID'], how='left')

rurality = pd.read_csv("../data/rurality.csv")

data = pd.merge(data, rurality, on='GEOID', how='left')
data['GEOID'] = data['GEOID'].astype(str).apply(lambda x: x.zfill(5))
data.sort_values(by=['GEOID', 'Year'], inplace=True)
data.to_csv("../data/merged_data_small.csv", index=False)

data_full = pd.merge(data_full, rurality, on='GEOID', how='left')
data_full['GEOID'] = data_full['GEOID'].astype(str).apply(lambda x: x.zfill(5))
data_full.sort_values(by=['GEOID', 'Year'], inplace=True)
data_full.to_csv("../data/merged_data.csv", index=False)