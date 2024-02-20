### Author: Ashlynn Wimer
### Date: 2/13/2024
### About: This script performs a spatial join on the geocoded hospitals dataset,
###        and uses the results of the join to add a GEOID key to the hospitals
###        DataFrame.

import geopandas as gpd
import pandas as pd

counties = gpd.read_file('../data/shapes/counties.shp')

def fix_hid(hid):
    '''
    The Geocoded dataset, due to an annoying issue in how they were constructed,
    have slightly flawed HIDs, in which some of the IDs have 6 characters (7
    expected). This function detects + fixes said HIDs.
    '''
    if len(hid) == 7:
        return hid
    else:
        fixed_nums = hid.split('H')[1].rjust(6, '0')
    return 'H' + fixed_nums

geocoded = pd.read_csv('../data/HospitalsGeocoded.csv')
geocoded = gpd.GeoDataFrame(
    geocoded,
    geometry=gpd.points_from_xy(geocoded.long, geocoded.lat, crs='EPSG:4326')
).to_crs(counties.crs)

# Three locations will fail to get a GEOID -- all are in PR, so we drop them.
geocoded = geocoded.sjoin(counties, how='left', predicate='within')
geocoded = geocoded[~geocoded['GEOID'].isna()]
geocoded['HID'] = geocoded['id'].apply(lambda x : fix_hid(x))
geocoded.drop('id', axis=1)

pd.read_csv('../data/HospitalAttributes.csv')\
    .merge(geocoded[['HID', 'GEOID']], how='inner', on='HID')\
    .to_csv('../data/HospitalAttributes.csv', index=False)

geocoded.drop(['id', 'Unnamed: 0', 'geometry'], axis=1).to_csv('../data/HospitalsGeocoded.csv', index=False)