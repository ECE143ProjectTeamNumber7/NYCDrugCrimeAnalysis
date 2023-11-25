import pandas as pd
import numpy as np
import requests
import glob
import os
import re
from bs4 import BeautifulSoup

def import_data(filenames = []):
    '''
    Imports datasets of all given filenames. 
    If filenames is empty, this will import all relevant dataset CSVs instead, i.e. Drug_Crime, and all 5 CSVs of 2020_Census/.
    
    Parameters:
        filenames (list):   Optional. List of CSV file names as strings. It is assumed that the filenames will be relative to the current directory.
                            If left empty or an empty list is passed in, it will import all relevant dataset CSVs located in data/
    
    Returns:
        List of datasets as a list tuple where datasets[0] is the file basename and datasets[1] is the pandas dataframe.
    '''
    assert isinstance(filenames, list)

    if len(filenames) == 0:
        filenames = [os.getcwd() + '/data/Drug_Crime_20231111.csv']
        filenames += glob.glob(os.getcwd() + '/data/2020_Census/*.csv')

    datasets = {}
    for filename in filenames:
        assert isinstance(filename, str)
        assert '.csv' in filename

        df = pd.read_csv(filename)
        
        label_loc = filename.find('Total-Population-')
        if 'Drug_Crime' in filename:
            datasets['Drug_Crime'] = df
        elif label_loc != -1:
            datasets[filename[label_loc + len('Total-Population-'):-4]] = df

    return datasets

def replace_column_nan(column, oldnan, newnan = np.nan):
    '''
    '''
    new_column = column.apply(lambda x: newnan if x == oldnan else x)
    
    return new_column
    

def convert_col_values(dataset, columns:list = [], conv_maps = [{}]):
    '''
    Renames data values in a column via a conversion table. Values not listed in the table are not converted and left as is.
    
    '''
    for col, conv_map in zip(columns, conv_maps):
        dataset[col] = dataset[col].map(conv_map, na_action="ignore")
        
    return dataset

def split_and_isolate(column, delim:str, part_index:int = None):
    '''
    '''
    data_split = column.str.split(delim)
    return data_split if part_index is None else data_split.str[part_index]

def get_time_day(dataset, merge:bool = False):    
    time_day_col = []
    for time in dataset['Time']:
        if 5 <= time.hour < 12:
            time_day_col.append('morning')
        elif 12 <= time.hour < 18:
            time_day_col.append('afternoon')
        else:
            time_day_col.append('night')
            
    if merge:
        dataset['Time of Day'] = time_day_col
        return dataset
    
    return pd.DataFrame({'Time of Day': time_day_col})

def get_precinct_info(dataset, merge:bool = False):
    def digit_extraction(col):
        numbers = re.findall(r'\d+', col)
        if numbers:
            return numbers[0]
        return None

    precincts = dataset['Precinct'].sort_values()
    precincts.unique()

    response = requests.get('https://www.nyc.gov/site/nypd/bureaus/patrol/precincts-landing.page')
    soup = BeautifulSoup(response.text, 'html.parser')
    table_class = 'rt'
    table = soup.find('table', {'class': table_class})

    if table:
        precincts_df = pd.read_html(str(table))[0]

    precincts_df.drop('Phone', axis = 1)

    precincts_df['Precinct'] = precincts_df['Precinct'].apply(digit_extraction)
    precincts_df = precincts_df.dropna(subset = 'Precinct')

    precincts_df.reset_index()

    precincts_df['Precinct'] = precincts_df['Precinct'].astype(int)

    if merge:
        return pd.merge(dataset, precincts_df, on = "Precinct", how = "left")
    
    return precincts_df
    
def preprocess_datasets(datasets):
    '''
    '''
    # Rename columns
    new_columns = {'CMPLNT_NUM': 'ID', 
                   'CMPLNT_FR_DT': 'Year', 
                   'CMPLNT_FR_TM': 'Time', 
                   'RPT_DT': 'Reported on:', 
                   'ADDR_PCT_CD': 'Precinct', 
                   'OFNS_DESC': 'Description', 
                   'CRM_ATPT_CPTD_CD': 'Completed?', 
                   'LAW_CAT_CD': 'Crime Category',
                   'PD_CD': 'NYC Penal Code',
                   'PD_DESC': 'Crime'}
    datasets['Drug_Crime'].rename(columns=new_columns, inplace=True)

    # Rearrange columns
    datasets['Drug_Crime'].drop(columns = ['CMPLNT_TO_TM', 'CMPLNT_TO_DT', 'Latitude', 'Longitude', 'KY_CD'], inplace = True)
    datasets['Drug_Crime'].set_index('ID', inplace = True)
    
    # Rename and drop NaN of relevant columns
    clean_cols = {'PARKS_NM': 'Not at a park', 
                  'LOC_OF_OCCUR_DESC': 'Location not known',
                  'HADEVELOPT': 'Not at a HA dev',
                  'BORO_NM': 'Borough not known',
                  'PREM_TYP_DESC': 'Premise not known'}
    for col in clean_cols:
        datasets['Drug_Crime'][col] = replace_column_nan(datasets["Drug_Crime"][col], oldnan='(null)').fillna(clean_cols[col])

    datasets['Drug_Crime'] = datasets['Drug_Crime'].drop(datasets['Drug_Crime'][datasets['Drug_Crime']['Time'] == '(null)'].index)    
    datasets['Drug_Crime'].dropna(inplace=True)

    # Fix crime to be more readable
    crimes = {'CONTROLLED SUBSTANCE,INTENT TO': 'POSS. OF CONTROLLED SUBSTANCE W/ INTENT TO SELL',
              'CONTROLLED SUBSTANCE, INTENT T': 'POSS. OF CONTROLLED SUBSTANCE W/ INTENT TO SELL',
              'CONTROLLED SUBSTANCE, POSSESSI': '7 DEG POSS. OF CONTROLLED',
              'CONTROLLED SUBSTANCE,POSSESS.': '3, 4, 5 DEG POSS. OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE,POSSESS.-': '1 & 2 DEG POSS. OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE, SALE 5': '5 DEG SALE OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE, SALE 4': '4 DEG SALE OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE,SALE 3': '3 DEG SALE OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE,SALE 2': '2 DEG SALE OF CONTROLLED SUBSTANCE',
              'CONTROLLED SUBSTANCE,SALE 1': '1 DEG SALE OF CONTROLLED SUBSTANCE',
              'MARIJUANA, POSSESSION 4 & 5': '4 & 5 DEG POSS. OF MARIJUANA',
              'MARIJUANA, SALE 4 & 5': '4 & 5 DEG SALE OF MARIJUANA',
              'MARIJUANA, POSSESSION 1, 2 & 3': '1, 2, 3 DEG POSS. OF MARIJUANA',
              'MARIJUANA, SALE 1, 2 & 3': '1, 2, 3 DEG SALE OF MARIJUANA',
              'DRUG PARAPHERNALIA,   POSSESSE': 'POSS. OF PARAPHERNALIA',
              'POSSESSION HYPODERMIC INSTRUME': 'POSS. OF HYPODERMIC INSTRUMENTS',
              'SALE SCHOOL GROUNDS 4': 'SALE SCHOOL GROUNDS',
              'SALE SCHOOL GROUNDS': 'SALE SCHOOL GROUNDS',
              'SALES OF PRESCRIPTION': 'SALES OF PRESCRIPTION',
              'UNDER THE INFLUENCE OF DRUGS': 'UNDER THE INFLUENCE OF DRUGS',
              'DRUG, INJECTION OF': 'INJECTION OF NARCOTICONTROLLED SUBSTANCE',
              'LOITERING 1ST DEGREE FOR DRUG': '1 DEG LOITERING FOR DRUGS',
              'USE CHILD TO COMMIT CONT SUB OFF': 'USE CHILD TO COMMIT CONTROLLED SUBSTANCE CRIMES',
              'POSS METH MANUFACT MATERIAL': 'POSS. OF METH MATERIALS'}
    datasets['Drug_Crime'] = convert_col_values(datasets['Drug_Crime'], columns=['Completed?', 'Crime'],
                                                conv_maps=[{'COMPLETED': True, 'ATTEMPTED': False}, crimes])
    
    # Parse dates for years only
    for col, delim, part in [('Year', '/', -1), ('Reported on:', '/', -1)]:
        datasets['Drug_Crime'][col] = split_and_isolate(datasets['Drug_Crime'][col], delim, part)
        
    # Convert time to DateTime and parse times for time of day and merge to original dataset
    datasets['Drug_Crime']['Time'] = pd.to_datetime(datasets['Drug_Crime']['Time'], format='%H:%M:%S').dt.time
    datasets['Drug_Crime'] = get_time_day(datasets['Drug_Crime'], merge=True)
    
    # Convert precinct numbers to the actual discernable precinct centers and details
    datasets['Drug_Crime'] = get_precinct_info(datasets['Drug_Crime'], merge=True)
    
    return datasets
        