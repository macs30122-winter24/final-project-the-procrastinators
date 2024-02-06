### Author: Ashlynn Wimer
### Date: 2/4/2024
### About: This script merges the IME_GME hospital datasets, the Hospital 
###        General Information Dataset, and the closure records to generate 
###        a large hospital attribute table. It also generates the CSV used 
###        for geocoding.

import pandas as pd
import re

###############################
###### Helper Functions #######
###############################

def clean_ime_gme(imegme, year, rename_table):
    '''
    Takes in an IME_GME dataframe, fills NAs where relevant,
    adds a year column, and applies a renaming schema

    Returns the cleaned dataframe
    '''
    # Add some relevant columns
    imegme[['IME1', 'DSH1']] = imegme[['IME1', 'DSH1']].fillna(0)
    imegme['Year'] = year

    imegme = imegme.rename(rename_table, axis=1)
    imegme['HID'] = imegme['HID'].apply(lambda x: 'H' + str(x).rjust(6, '0'))
    imegme[['DispropShareHospitalAdj', 'IndirectMedicalEducationAdj', 'TotalEmployees', 
                            'TotalBeds', 'TotalMedicareDays', 'TotalMedicaidDays', 'TotalDays', 
                            'TotalMedicareDischarges', 'TotalMedicaidDischarges', 'TotalDischarges']]\
                            .isna().sum()
    return imegme

def clean_text(text):
    '''
    Helper function which does basic text cleaning to enable record linkage
    '''
    return re.sub(r"[',-.]", '', text).upper().strip()

def has_match(closure, ime_to_match):
    '''
    Function which check if a closed hospital has a matching entry *anywhere*
    in the IME_GME datasets by comparing CityState pairs, Zips, and hospital Names.

    Note: This function assumes that one has double checked that there are not
    near duplicates in the closure dataset; specifically, all City/State pairs
    must be unique, and all zips must be unique. If they are not, then this 
    function will report matches that are fake.
    
    Inputs:
      closure: row from the 'closures' dataset. Assumes presence
        of the following columns:
          Zip, CityState, Hospital
      imegmes: dataframe of id variables from imegmes. Assumes at minimum presence of the following 
        columns:
          Zip, CityState, Name
    
    If there is a match, returns True
    '''
    if clean_text(closure['CityState']) in ime_to_match['CityState'].to_list():
        return True
    
    if clean_text(closure['Hospital']) in ime_to_match['Name'].to_list():
        return True
    
    if closure['Zip'] in ime_to_match['Zip'].apply(lambda x: str(x).strip('-')).to_list():
        num_mtch = sum(ime_to_match['Zip'].apply(lambda x: str(x).strip('-')) == closure['Zip'])
        if num_mtch > 1:
            print(f'Zip {closure["Zip"]} may require hand coding to determine a match')
        return True
    
    return False

def get_match(closure, ime_to_match):
    '''
    Function which, given a closed hospital *with* a match in the ime_to_match dataset,
     return the relevant HID.

    Note: This function assumes that one has double checked that there are not
     near duplicates in the closure dataset; specifically, all City/State pairs
     must be unique, and all zips must be unique. If they are not, then this 
     function will report matches that are fake.
    
    Inputs:
      closure: row from the 'closures' dataset. Assumes presence
        of the following columns:
          Zip, CityState, Hospital
      imegmes: dataframe of id variables from imegmes. Assumes at minimum presence of the following 
        columns:
          Zip, CityState, Name
    
    Returns matching HID. Otherwise, yells at you.
    '''
    if clean_text(closure['CityState']) in ime_to_match['CityState'].to_list():
        matching_hid = ime_to_match[\
            ime_to_match['CityState'] == clean_text(closure['CityState'])]['HID']
        return matching_hid
    
    if clean_text(closure['Hospital']) in ime_to_match['Name'].to_list():
        matching_hid = ime_to_match[\
            ime_to_match['Name'] == clean_text(closure['Hospital'])]['HID']
        return matching_hid
    
    if closure['Zip'] in ime_to_match['Zip'].to_list():
        matching_hid = ime_to_match[ime_to_match['Zip'] == closure['Zip']]['HID']
        return matching_hid
    
    assert False, f'The following closure has no matching value in the ime_to_gme\n{closure}'

### Below, we read in, clean, and eventually merge our three datasets.
### This takes a bit of record linkage effort, so there is a *lot* of cleaning,
### and the resultant dataset is still a bit messy.
    
### First, we clean the IME_GME files

## Helper constants
RELEVANT_COLUMNS = [
    'PROVIDER_NUMBER', 'HOSPITAL_Name', 'Street_Addr', 
    'City', 'State', 'Zip_Code', 'DSH1', 'IME1', 
    'TOTAL_HOSPITAL_EMPLOYEES_ON_PAYROL',
    'TOTAL_HOSPITAL_BEDS', 'TOTAL_HOSPITAL_MEDICARE_DAYS', 
    'TOTAL_HOSPITAL_MEDICAID_DAYS', 'TOTAL_HOSPITAL_DAYS', 
    'TOTAL_HOSPITAL_MEDICARE_DISCHARGES', 'TOTAL_HOSPITAL_MEDICAID_DISCHARGES', 
    'TOTAL_HOSPITAL_DISCHARGES'
]

RENAME_TABLE = {
    'PROVIDER_NUMBER':'HID',
    'HOSPITAL_Name':'Name',
    'Street_Addr':'Address',
    'Zip_Code':'Zip',
    'TOTAL_HOSPITAL_EMPLOYEES_ON_PAYROL':'TotalEmployees',
    'TOTAL_HOSPITAL_BEDS':'TotalBeds',
    'TOTAL_HOSPITAL_MEDICARE_DAYS':'TotalMedicareDays',
    'TOTAL_HOSPITAL_MEDICAID_DAYS':'TotalMedicaidDays',
    'TOTAL_HOSPITAL_DAYS':'TotalDays',
    'TOTAL_HOSPITAL_MEDICARE_DISCHARGES':'TotalMedicareDischarges',
    'TOTAL_HOSPITAL_MEDICAID_DISCHARGES':'TotalMedicaidDischarges',
    'TOTAL_HOSPITAL_DISCHARGES':'TotalDischarges',
    'IME1':'IndirectMedicalEducationAdj',
    'DSH1':'DispropShareHospitalAdj'
}

# Create the actual IME_GME file
ime_gmes = []
for i in range(10, 24):
    ime_gme = pd.read_csv(f'../data/raw/hospitals/IME_GME/IME_GME20{i}.csv')[RELEVANT_COLUMNS]
    ime_gmes.append(clean_ime_gme(ime_gme, f'20{i}', RENAME_TABLE))

# Save this WIP dataset as our target for geocoding
big_ime_gme = pd.concat(ime_gmes, ignore_index=True).drop_duplicates()
big_ime_gme.drop('Zip', axis=1).to_csv('../data/raw/hospitals/IME_GME_Comp.csv', index=False)


## Now that the IME_GME datasets are clean, we clean the hospital general
## information dataset.

# Read in additional rows of info
hosps = pd.read_csv('../data/raw/hospitals/Hospital_General_Information.csv')
hosps = hosps.rename({
    'Facility ID':'HID',
    'Facility Name':'Name',
    'City/Town':'City',
    'Hospital Type':'HospitalType',
    'Emergency Services':'HasEmergencyServices',
    'Meets criteria for birthing friendly designation':'HasBirthingFriendlyDesignation'
}, axis=1)[['HID', 'Name', 'Address', 'City', 'State', 'HospitalType', 'HasEmergencyServices', 'HasBirthingFriendlyDesignation']]

# Apply our Merge ID rules on it, do some variable adjusting
hosps['HID'] = hosps['HID'].apply(lambda x: 'H' + str(x).rjust(6, '0'))
hosps['HasEmergencyServices'] = hosps['HasEmergencyServices']\
    .apply(lambda x: 1 if x=='Yes' else 0)
hosps['HasBirthingFriendlyDesignation'] = hosps['HasBirthingFriendlyDesignation']\
    .apply(lambda x: 1 if x=='Y' else 0)
hosps['Year'] = 'NA'

## Closures:
## The above two datasets are natively (but imperfectly) linked through the 
## HID. This dataset is *not* linked to them, so we have to manually perform
## a record linkage.
## We will lose five values from our larger dataframe, but (as this is a short 
## term project), that seems like an acceptable number of hospitals to drop.

# Make the dataset for a record linkage
ime_to_match = big_ime_gme.copy()[['Name', 'Zip', 'City', 'State', 'HID']]
ime_to_match['CityState'] = ime_to_match['City'].apply(clean_text) + ime_to_match['State'].apply(clean_text)
ime_to_match['Zip'] = ime_to_match['Zip'].apply(lambda x: str(x).split('-')[0])
ime_to_match = ime_to_match.drop_duplicates('HID').reset_index().drop('index', axis=1)

# Read in and preliminarily clean closures
closures = pd.read_excel('../data/raw/hospitals/Closures-Database-for-Web.xlsx',
                          dtype={'Zip':str})

closures = closures\
    .drop(columns=['Count', 'updated 1/11/2024', 'RUCA', 'CBSA'])\
    .dropna()\
    .rename(
        {
            "Complete Closure (0);\nConverted Closure (1)":"Converted",
            'Closure Month':'ClosureMonth',
            'Closure Year':'ClosureYear'
        }, axis=1
    )

# Our study period does not consider hospitals outside this range
closures = closures[closures['ClosureYear'] >= 2011]

# Get matches
closures['CityState'] = closures['City'].apply(clean_text) + closures['State'].apply(clean_text)
matches = [has_match(closure[1], ime_to_match) for closure in closures.iterrows()]
matched = closures[matches].copy()

# Get the HIDs for the matches
HIDS = []
for row in matched.iterrows():
    HIDS.append(get_match(row[1], ime_to_match).to_list()[0])
matched['HID'] = HIDS

# Do a bit of cleaning
matched = matched.reset_index(drop=True).drop(columns=['CityState', 'County/district'])

# Variable to indicate that _these_ are the closed hospitals
matched['HasClosed'] = 1

# Make the big attribute table
hosp_attr = big_ime_gme.merge(matched.drop(columns=['Hospital', 'Address', 'City', 'State', 'Zip']), how='left', on='HID')\
    .merge(hosps.drop(columns=['Name', 'Address', 'City', 'State', 'Year']), how='left', on='HID')\
    .reset_index(drop=True)

# Light cleaning
hosp_attr['HasClosed'] = hosp_attr['HasClosed'].fillna(0)

# Save for personal use
hosp_attr.to_csv('../data/HospitalAttributesWide.csv', index=False)

# Tidyify and save for project use
hosp_attr_tidy = hosp_attr.melt(
    id_vars=['HID', 'Name', 'Address', 'City', 'State', 'Year', 'Zip']
)
hosp_attr_tidy.to_csv('../data/HospitalAttributes.csv', index=False)
