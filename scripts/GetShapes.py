### Author: Ashlynn Wimer
### Date: 2/2/2024
### About: Script to retrieve and clean county, county subdivision shapefiles.
import geopandas as gpd
import pandas as pd
import pygris

# Get the shape of all counties nationwide
# cb=True means that we aren't getting the annoying
# shapes that include area *over waterways*
counties = pygris.counties(cb=True, cache=True)
counties = counties[['GEOID', 'NAME', 'NAMELSAD', 'STATE_NAME', 'geometry']]
counties.to_file('../data/shapes/counties.shp')

# Get the shape of all county subdivisions nationwide
# County subdivisions must be pulled per state
# so we do a little bit more work.
states = counties[['STATEFP']].drop_duplicates()
county_subs = pygris.county_subdivisions(state=states.loc[0, 'STATEFP'], cb=True)
for state in states.loc[1:, 'STATEFP']:
    print(state)
    county_subs = pd.concat([county_subs, pygris.county_subdivisions(state=state, cb=True)], ignore_index=True)
county_subs = county_subs[['GEOID', 'NAME', 'NAMELSAD', 'STATE_NAME', 'geometry']]
county_subs.to_file('../data/shapes/county_subdivisions.shp')