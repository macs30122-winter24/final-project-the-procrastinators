import pandas as pd
import os
path = '/Users/dingxuzhou/Documents/Uchi/MACSS 30122/final project/'
files = os.listdir(path)
inflow_files = [file for file in files if 'countyinflow' in file.lower()]
outflow_files = [file for file in files if 'countyoutflow' in file.lower()]

# Initialize separate DataFrames for inflow and outflow
inflow_df = pd.DataFrame(columns=['Year', 'GEOID', 'Inflow_Household', 'Inflow_Individual', 'Inflow_AGI'])
outflow_df = pd.DataFrame(columns=['Year', 'GEOID', 'Outflow_Household', 'Outflow_Individual', 'Outflow_AGI'])

def make_sure_digits(df, column_name, digits):
    df[column_name] = df[column_name].apply(lambda x: x.zfill(digits))
    return df

# Process Inflow Files
for inflow_file in inflow_files:
    file_path = os.path.join(path, inflow_file)
    df = pd.read_csv(file_path, dtype={'y2_statefips': str, 'y2_countyfips': str, 'y1_statefips': str, 'y1_countyfips': str}, encoding='latin1')
    make_sure_digits(df, 'y2_statefips', 2)
    make_sure_digits(df, 'y2_countyfips', 3)
    make_sure_digits(df, 'y1_statefips', 2)
    make_sure_digits(df, 'y1_countyfips', 3)
    df['GEOID'] = df['y2_statefips'] + df['y2_countyfips']
    df['y1_id'] = df['y1_statefips'] + df['y1_countyfips']
    df = df.drop(['y2_statefips', 'y2_countyfips', 'y1_statefips', 'y1_countyfips', 'y1_state'], axis=1)
    filtered_df = df[df['y1_countyname'].str.contains('County Total Migration-US and Foreign')]
    summed_df = filtered_df.groupby('GEOID').agg({'n1': 'sum', 'n2': 'sum', 'agi': 'sum'}).reset_index()
    summed_df = summed_df.rename(columns={'GEOID': 'GEOID', 'n1': 'Inflow_Household', 'n2': 'Inflow_Individual', 'agi': 'Inflow_AGI'})
    year = '20' + inflow_file[-8:-6]
    summed_df['Year'] = year
    inflow_df = pd.concat([inflow_df, summed_df[['Year', 'GEOID', 'Inflow_Household', 'Inflow_Individual', 'Inflow_AGI']]], ignore_index=True)

# Process Outflow Files
for outflow_file in outflow_files:
    file_path = os.path.join(path, outflow_file)
    df = pd.read_csv(file_path, dtype={'y2_statefips': str, 'y2_countyfips': str, 'y1_statefips': str, 'y1_countyfips': str}, encoding='latin1')
    make_sure_digits(df, 'y2_statefips', 2)
    make_sure_digits(df, 'y2_countyfips', 3)
    make_sure_digits(df, 'y1_statefips', 2)
    make_sure_digits(df, 'y1_countyfips', 3)
    df['GEOID'] = df['y1_statefips'] + df['y1_countyfips']
    df['y2_id'] = df['y2_statefips'] + df['y2_countyfips']
    df = df.drop(['y2_statefips', 'y2_countyfips', 'y1_statefips', 'y1_countyfips', 'y2_state'], axis=1)
    filtered_df = df[df['y2_countyname'].str.contains('County Total Migration-US and Foreign')]
    summed_df = filtered_df.groupby('GEOID').agg({'n1': 'sum', 'n2': 'sum', 'agi': 'sum'}).reset_index()
    summed_df = summed_df.rename(columns={'GEOID': 'GEOID', 'n1': 'Outflow_Household', 'n2': 'Outflow_Individual', 'agi': 'Outflow_AGI'})
    year = '20' + outflow_file[-8:-6]  # Corrected variable name here
    summed_df['Year'] = year
    outflow_df = pd.concat([outflow_df, summed_df[['Year', 'GEOID', 'Outflow_Household', 'Outflow_Individual', 'Outflow_AGI']]], ignore_index=True)

# Merge inflow and outflow DataFrames based on 'GEOID' and 'Year'
combined_df = pd.merge(inflow_df, outflow_df, on=['Year', 'GEOID'], how='left')
combined_df = combined_df.fillna(0)
output_path = '/Users/dingxuzhou/Documents/Uchi/MACSS 30122/final project/irs_data.csv'
combined_df.to_csv(output_path, index=False)