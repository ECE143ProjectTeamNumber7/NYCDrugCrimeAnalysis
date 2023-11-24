import pandas as pd
import numpy as np
import glob
import os

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
    
    # datasets['Drug_Crime']['Completed?'] = datasets['Drug_Crime']['Completed?'].map({'COMPLETED': True, 'ATTEMPTED': False})
    
    return dataset

def isolate_date_part(data, columns:list, date_part:str):
    '''
    '''
    part_index = {'m': 0, 'd': 1, 'y': 2}
    assert date_part in part_index.keys()
    
    for col in columns:
        data[col] = data[col].str.split('/').str[part_index[date_part]]
        
    return data

def preprocess_datasets(datasets):
    '''
    '''
    # Clean NaN of relevant columns
    datasets['Drug_Crime']['PARKS_NM'] = replace_column_nan(datasets["Drug_Crime"]['PARKS_NM'], oldnan='(null)').fillna('Not at a park')
    
    # Rename columns
    new_columns = {'CMPLNT_NUM': 'ID', 
                   'CMPLNT_FR_DT': 'Year', 
                   'CMPLNT_FR_TM': 'Time', 
                   'CMPLNT_TO_DT': 'EndYear', 
                   'RPT_DT': 'Reported on:', 
                   'ADDR_PCT_CD': 'Precinct', 
                   'OFNS_DESC': 'Description', 
                   'CRM_ATPT_CPTD_CD': 'Completed?', 
                   'LAW_CAT_CD': 'Charge_Type',
                   'PD_CD': 'NYC Penal Code',
                   'PD_DESC': 'Crime'}
    datasets['Drug_Crime'].rename(columns=new_columns, inplace=True)

    # Rearrange Columns
    datasets['Drug_Crime'].drop(columns = ['CMPLNT_TO_TM', 'Latitude', 'Longitude', 'KY_CDs'], inplace = True)
    datasets['Drug_Crime'].set_index('ID', inplace = True)
    
    # Adjust Column Values To Valid Readable Data
    isolate_date_part(datasets['Drug_Crime'], ['Year', 'Reported on:', 'EndYear'], 'y')
    crimes = {'CONTROLLED SUBSTANCE,INTENT TO': 'POSSESS. OF CS W/ INTENT TO SELL',
              'CONTROLLED SUBSTANCE, INTENT T': 'POSSESS. OF CS W/ INTENT TO SELL',
              'CONTROLLED SUBSTANCE, POSSESSI': '7 DEG POSSESS. OF CS',
              'CONTROLLED SUBSTANCE,POSSESS.': '3, 4, 5 DEG POSSESS. OF CS',
              'CONTROLLED SUBSTANCE,POSSESS.-': '1 & 2 DEG POSSESS. OF CS',
              'CONTROLLED SUBSTANCE, SALE 5': '5 DEG SALE OF CS',
              'CONTROLLED SUBSTANCE, SALE 4': '4 DEG SALE OF CS',
              'CONTROLLED SUBSTANCE,SALE 3': '3 DEG SALE OF CS',
              'CONTROLLED SUBSTANCE,SALE 2': '2 DEG SALE OF CS',
              'CONTROLLED SUBSTANCE,SALE 1': '1 DEG SALE OF CS',
              'MARIJUANA, POSSESSION 4 & 5': '4 & 5 DEG POSSESS. OF MARIJUANA',
              'MARIJUANA, SALE 4 & 5': '4 & 5 DEG SALE OF MARIJUANA',
              'MARIJUANA, POSSESSION 1, 2 & 3': '1, 2, 3 DEG POSSESS. OF MARIJUANA',
              'MARIJUANA, SALE 1, 2 & 3': '1, 2, 3 DEG SALE OF MARIJUANA',
              'DRUG PARAPHERNALIA,   POSSESSE': 'POSSESS. OF PARAPHERNALIA',
              'POSSESSION HYPODERMIC INSTRUME': 'POSSESS. OF HYPODERMIC INSTRUMENTS',
              'SALE SCHOOL GROUNDS 4': 'SALE SCHOOL GROUNDS',
              'SALE SCHOOL GROUNDS': 'SALE SCHOOL GROUNDS',
              'SALES OF PRESCRIPTION': 'SALES OF PRESCRIPTION',
              'UNDER THE INFLUENCE OF DRUGS': 'UNDER THE INFLUENCE OF DRUGS',
              'DRUG, INJECTION OF': 'INJECTION OF NARCOTICS',
              'LOITERING 1ST DEGREE FOR DRUG': '1 DEG LOITERING FOR DRUGS',
              'USE CHILD TO COMMIT CONT SUB OFF': 'USE CHILD TO COMMIT CS CRIMES',
              'POSS METH MANUFACT MATERIAL': 'POSSESS. OF METH MATERIALS'}
    datasets['Drug_Crime'] = convert_col_values(datasets['Drug_Crime'], columns=['Completed?', 'Crime'],
                                                conv_maps=[{'COMPLETED': True, 'ATTEMPTED': False}, crimes])
    
    return datasets
        