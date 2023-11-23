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
    

def convert_data(data, conv_table = {}):
    '''
    Converts the data type of the respective column in the dataframe to the corresponding datatype, inplace. Original dataframe will be returned.
    Useful for when a column of the pandas dataframe is a `str` object, but should or can be converted to an actual Python datatype.
    e.g. Converting 08/27/2001 `str` object to `DateTime` object.

    Parameters:
        data (pd.DataFrame):    Dataframe of which the columns shall be modified.
        conv_table (dict):      Optional. Dictionary off column names as the key and datatype as the value
    
    Returns:
        Original pandas dataframe to be used for reference or discarded.
    '''
    pass

def isolate_date_part(data, columns:list, date_part:str):
    part_index = {'m': 0, 'd': 1, 'y': 2}
    assert date_part in part_index.keys()
    
    for col in columns:
        data[col] = data[col].str.split('/').str[part_index[date_part]]
        
    return data

def preprocess_datasets(datasets):
    # Clean NaN of relevant columns
    datasets['Drug_Crime']['PARKS_NM'] = replace_column_nan(datasets["Drug_Crime"]['PARKS_NM'], oldnan='(null)').fillna('Not at a park')
    
    # Rename columns
    new_columns = {'CMPLNT_NUM': 'ID', 'CMPLNT_FR_DT': 'Year', 'CMPLNT_FR_TM': 'Time', 'CMPLNT_TO_DT': 'EndYear', 
                        'RPT_DT': 'Reported on:', 'ADDR_PCT_CD': 'Precinct', 'KY_CD': 'Offense_Code',
                        'OFNS_DESC': 'Description', 'CRM_ATPT_CPTD_CD': 'Completed?'}
    datasets['Drug_Crime'].rename(columns=new_columns, inplace=True)

    # Rearrange Columns
    datasets['Drug_Crime'].drop(columns = ['CMPLNT_TO_TM', 'Latitude', 'Longitude'], inplace = True)
    datasets['Drug_Crime'].set_index('ID', inplace = True)
    
    # Adjust Column Values
    isolate_date_part(datasets['Drug_Crime'], ['Year', 'Reported on:', 'EndYear'], 'y')
    datasets['Drug_Crime']['Completed?'] = datasets['Drug_Crime']['Completed?'].map({'COMPLETED': True, 'ATTEMPTED': False})
    
    # Drop Redundant Columns NOTE: Compute via Pearson's and Visualize Correlation by Scatter plot or some other method.
    datasets['Drug_Crime'].drop(columns = ['Offense_Code', 'LAW_CAT_CD'], inplace = True)

    # TODO: Isolate Drug Crime Possession Type
    pd_desc_mapping = {'CONTROLLED SUBSTANCE,POSSESS.', 'CONTROLLED SUBSTANCE, POSSESSI' }
    
    return datasets
        