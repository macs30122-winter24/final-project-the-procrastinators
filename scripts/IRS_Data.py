import os
import pandas as pd
def process_files(files, flow_type):
    '''
    Process the inflow or outflow files and return a dataframe:

    Input:
    - files: list of file names
    - flow_type: 'inflow' or 'outflow'

    Output:
    - df_list: list of dataframes

    '''
    df_list = []
    for file in files:
        file_path = os.path.join(path, file)
        df = pd.read_csv(file_path, dtype={'y2_statefips': str, 'y2_countyfips': str, 'y1_statefips': str, 'y1_countyfips': str}, encoding='latin1')
        make_sure_digits(df, 'y2_statefips', 2)
        make_sure_digits(df, 'y2_countyfips', 3)
        make_sure_digits(df, 'y1_statefips', 2)
        make_sure_digits(df, 'y1_countyfips', 3)

        cols_map = {
            'inflow': {
                'geo_cols': ('y2_statefips', 'y2_countyfips'),
                'id_cols': ('y1_statefips', 'y1_countyfips'),
                'countyname_col': 'y1_countyname',
                'drop_cols': ('y2_statefips', 'y2_countyfips', 'y1_statefips', 'y1_countyfips', 'y1_state')
            },
            'outflow': {
                'geo_cols': ('y1_statefips', 'y1_countyfips'),
                'id_cols': ('y2_statefips', 'y2_countyfips'),
                'countyname_col': 'y2_countyname',
                'drop_cols': ('y1_statefips', 'y1_countyfips', 'y2_statefips', 'y2_countyfips', 'y2_state')
            }
        }
        geo_cols, id_cols, countyname_col, drop_cols = cols_map[flow_type].values()
        household_col, individual_col, agi_col = 'n1', 'n2', 'agi'
        
        df['GEOID'] = df[geo_cols[0]] + df[geo_cols[1]]
        df['id'] = df[id_cols[0]] + df[id_cols[1]]
        df = df.drop(list(drop_cols), axis=1)
        
        filtered_df = df[df[countyname_col].str.contains('County Total Migration-US and Foreign')]
        summed_df = filtered_df.groupby('GEOID').agg({household_col: 'sum', individual_col: 'sum', agi_col: 'sum'}).reset_index()
        summed_df.columns = ['GEOID', f'{flow_type.capitalize()}_Household', f'{flow_type.capitalize()}_Individual', f'{flow_type.capitalize()}_AGI']
        
        year = '20' + file[-8:-6]
        summed_df['Year'] = year
        df_list.append(summed_df[['Year', 'GEOID', f'{flow_type.capitalize()}_Household', f'{flow_type.capitalize()}_Individual', f'{flow_type.capitalize()}_AGI']])
    
    return pd.concat(df_list, ignore_index=True)

def make_sure_digits(df, column_name, digits):
    df[column_name] = df[column_name].apply(lambda x: x.zfill(digits))
    return df

path = '/Users/dingxuzhou/Documents/Uchi/MACSS 30122/final project/'
output_path = os.path.join(path, 'irs_data.csv')

files = os.listdir(path)
inflow_files = [file for file in files if 'countyinflow' in file.lower()]
outflow_files = [file for file in files if 'countyoutflow' in file.lower()]

inflow_df = process_files(inflow_files, 'inflow')
outflow_df = process_files(outflow_files, 'outflow')

combined_df = pd.merge(inflow_df, outflow_df, on=['Year', 'GEOID'], how='left').fillna(0)
combined_df.to_csv(output_path, index=False)