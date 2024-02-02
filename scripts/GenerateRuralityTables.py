## Author: Ashlynn Wimer
## Date: 1/26/2024
## About: Python script used to generate two varities of rurality tables for
##        every coutny within my study area. 
## Note: This script is *heavily* based on one used for MACS 30100. The main
##       addition to this script is the revised export format (i.e. from 
##       wide format to tidy format).

import pandas as pd

def bin_rurality(secondary_code):
    '''
    Quick helper function for converting RUCA codes to Rural, Urban,
    or Suburban classifications. Uses the OEPS classifications.
    '''
    match (secondary_code):
        case 1.0 | 1.1:
            return 'RucaUrban'
        case 2.0 | 2.1 | 4.0 | 4.1:
            return 'RucaSuburban'
        case _:
            return 'RucaRural'

#### Read in

# Ruralities
cdc_rurality = pd.read_csv('../data/raw/rurality/NCHSURCodes2013.csv',
                           dtype={'FIPS code':str})
ruca_rurality = pd.read_csv('../data/raw/rurality/ruca2010revised.csv',\
                            dtype={'State-County FIPS Code':str, 'Primary RUCA Code 2010':str})

far_rurality = pd.read_csv('../data/raw/rurality/FARcodesZIPdata2010WithAKandHI.csv',
                           dtype={'ZIP':str})

# Helper dataset
zip_county_crosswalk = pd.read_csv('../data/raw/crosswalks/ZIP_COUNTY_122010.csv',
                                   dtype={'ZIP':str, 'COUNTY':str})

#### Transform and select attributes

## CDC
cdc_rurality = cdc_rurality.rename({'FIPS code':'GEOID', '2013 code':'CdcRurality'}, axis=1)
cdc_rurality['GEOID'] = cdc_rurality['GEOID'].apply(lambda x: x.rjust(5, '0'))
cdc_rurality = cdc_rurality[['GEOID', 'CdcRurality']]

## RUCA
ruca_rurality = ruca_rurality.rename({'State-County FIPS Code':'GEOID',
                      'Secondary RUCA Code, 2010 (see errata)': 'RucaRurality'},
                      axis=1)
ruca_rurality['RucaRurality'] = ruca_rurality['RucaRurality'].apply(lambda x: bin_rurality(x))
ruca_rurality = ruca_rurality[['GEOID', 'RucaRurality']]
ruca_rurality = pd.get_dummies(ruca_rurality['RucaRurality'])\
    .groupby(ruca_rurality['GEOID'])\
    .sum()\
    .reset_index()

## FAR
far_rurality['far1'] = far_rurality['far1'].apply(lambda x: 'FAR' if x==1 else 'NOT')
far_rurality = far_rurality[['ZIP', 'far1']]

far_rurality = far_rurality.merge(zip_county_crosswalk, on='ZIP', how='inner')
far_rurality = pd.get_dummies(far_rurality['far1'])\
    .groupby(far_rurality['COUNTY'])\
    .sum()\
    .reset_index()

far_rurality['FarP'] = 100 * far_rurality['FAR'] / (far_rurality['NOT'] + far_rurality['FAR'])
far_rurality = far_rurality.rename({'COUNTY':'GEOID'}, axis=1)
far_rurality = far_rurality[['GEOID', 'FarP']]

#### Merge and Filter
rurality = far_rurality\
    .merge(ruca_rurality, how='inner', on='GEOID')\
    .merge(cdc_rurality, how='inner', on='GEOID')

## TODO: Pivot to tidy format.

rurality = pd.melt(rurality, id_vars='GEOID',\
                   value_vars=['CdcRurality', 'RucaRural', \
                               'RucaSuburban', 'RucaUrban', 'FarP'])

#### Save
rurality.to_csv('../data/rurality.csv', index=False)
