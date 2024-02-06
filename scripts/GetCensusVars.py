### Author: Dan Gilles
### Date: 2/5/2024
### Description: This script gets variable names and explanations from the census API and saves them to a csv file.

import requests                
import pandas as pd

# get variables from the census api
for census_type in ['acs1', 'acs5', 'acsse']:
    url = f"https://api.census.gov/data/2022/acs/{census_type}/variables.json"
    r = requests.get(url)
    data = r.json()
    df = pd.DataFrame(data['variables']).T
    df = df[['label', 'concept']]
    df = df.sort_values(by='concept')
    df.to_csv(f"../data/variables/census_variables_{census_type}.csv")
    print(f"Saved {census_type} variables to csv")