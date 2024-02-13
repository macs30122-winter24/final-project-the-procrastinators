### Author: Dan Gilles
### Date: 2/13/2024
### Description: This script gets the data from the IRS and Census Bureau and merges it into one file.

import pandas as pd

meanings = ['Total Population', 'Labor Force', 'Unemployed', 'Median Income']
census_types = ['acs1', 'acs5', 'acsse']
data = pd.read_csv("../data/irs_data.csv")

for census_type in census_types:
    counties = pd.read_csv(f"../data/census_data_{census_type}.csv")
    meanings2 = [m + ' (' + census_type.upper() + ')' for m in meanings]
    counties.rename(columns=dict(zip(meanings, meanings2)), inplace=True)
    data = pd.merge(data, counties, on=['Year', 'GEOID'])

data.sort_values(by=['GEOID', 'Year'], inplace=True)

data.to_csv("../data/merged_data.csv", index=False)