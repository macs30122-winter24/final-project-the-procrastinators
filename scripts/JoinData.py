### Author: Dan Gilles
### Date: 2/13/2024
### Description: This script joins the merged IRS, ACS and rurality data
###              with the hospital data to create a single dataset for analysis.

import pandas as pd

data = pd.read_csv("../data/merged_data.csv")
hospitals = pd.read_csv("../data/HospitalAttributes.csv")

joined = pd.merge(hospitals, data, on=['GEOID', 'Year'], how='left')

years = joined.pop('Year')
joined.insert(1, 'Year', years)
joined.sort_values(by=['HID', 'Year'], inplace=True)

joined.to_csv("../data/joined_data.csv", index=False)