import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
from ast import literal_eval

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
        return dataset.reset_index().merge(precincts_df, on = 'Precinct', how='left').set_index('ID')
    
    return precincts_df

def clean_missing_boroughs(dataset, validity_threshold = 0.2):
    grouped_dataset = dataset.groupby('BORO_NM')
    
    precinct_map = {}
    for borough, group in grouped_dataset:
        if borough == 'Borough not known':
            target_indices = list(group.index)
        else:
            precinct_counts = group['Precinct'].value_counts()
            counts = list(precinct_counts.to_dict().values())  # get counts of all precinct in descending order
            drop_index = 0
            for i in range(1, len(counts)):
                if counts[i] / counts[i - 1] < validity_threshold:
                    drop_index = i
                    break
            
            for index, value in zip(list(range(0, len(counts))), precinct_counts.items()):
                if index < drop_index:
                    precinct_map[value[0]] = borough

    for target in target_indices:
        target_precinct = dataset.loc[target, 'Precinct']
        if target_precinct in precinct_map.keys():
            dataset.loc[target, 'BORO_NM'] = precinct_map[target_precinct]

    # TODO: DROP REMAINING UNKNOWN
    dataset = dataset[dataset['BORO_NM'] != 'Borough not known']

    return dataset

def preprocess_drug_crime(dataset):
    try:
        # Rename columns
        new_columns = {'CMPLNT_NUM': 'ID', 
                    'CMPLNT_FR_DT': 'Date', 
                    'CMPLNT_FR_TM': 'Time', 
                    'RPT_DT': 'Reported on:', 
                    'ADDR_PCT_CD': 'Precinct', 
                    'OFNS_DESC': 'Description', 
                    'CRM_ATPT_CPTD_CD': 'Completed?', 
                    'LAW_CAT_CD': 'Crime Category',
                    'PD_CD': 'NYC Penal Code',
                    'PD_DESC': 'Crime'}
        dataset.rename(columns=new_columns, inplace=True)

        # Rearrange columns
        dataset.drop(columns = ['CMPLNT_TO_TM', 'CMPLNT_TO_DT', 'Latitude', 'Longitude', 'KY_CD'], inplace = True, errors='ignore')
        dataset.set_index('ID', inplace = True)
        
        # Rename and drop NaN of relevant columns
        clean_cols = {'PARKS_NM': 'Not at a park', 
                    'LOC_OF_OCCUR_DESC': 'Location not known',
                    'HADEVELOPT': 'Not at a HA dev',
                    'BORO_NM': 'Borough not known',
                    'PREM_TYP_DESC': 'Premise not known'}
        for col in clean_cols:
            dataset[col] = replace_column_nan(dataset[col], oldnan='(null)').fillna(clean_cols[col])

        dataset = dataset.drop(dataset[dataset['Time'] == '(null)'].index)    
        dataset.dropna(inplace=True)

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
        dataset = convert_col_values(dataset, columns=['Completed?', 'Crime'],
                                                    conv_maps=[{'COMPLETED': True, 'ATTEMPTED': False}, crimes])
        
        # Parse dates for years and months and set to its own column and convert to int
        for col, new_col, delim, part in [('Date', 'Year', '/', 2), ('Date', 'Month', '/', 0), ('Reported on:', 'Reported on:', '/', -1)]:
            dataset[new_col] = split_and_isolate(dataset[col], delim, part)
            dataset[new_col] = dataset[new_col].astype('int64')
            
        # Convert time to DateTime and parse times for time of day and merge to original dataset
        dataset['Time'] = pd.to_datetime(dataset['Time'], format='%H:%M:%S').dt.time
        dataset = get_time_day(dataset, merge=True)

        # Convert Lat_Long from string to tuple
        dataset['Lat_Lon'] = dataset['Lat_Lon'].apply(lambda x: eval(x))

        # Convert precinct numbers to the actual discernable precinct centers and details
        dataset = get_precinct_info(dataset, merge=True)
    except:
        raise Exception('An invalid dataset with vital columns missing was provided, please provide a valid (unprocessed) Drug_Crime dataset!')
    return dataset

def preprocess_census(datasets:dict):
    try:
        population_col_filter = re.compile('.*_[0-9]+')
        merged_census = pd.DataFrame()
        for race in datasets:
            if merged_census.empty: # If any of the columns does not exist, this will raise an error to be caught to raise an invalid dataset exception
                for col in ['GeoID', 'GeoType', 'Borough', 'GeoID', 'Name']:
                    merged_census[col] = datasets[race][col]
            
            # Rename columns
            rename_cols = {'Pop Change': f'{race} Pop Change', 'Natural Change': f'{race} Natural Change', 'Net Migration': f'{race} Net Migration'}
            for name in list(filter(population_col_filter.match, datasets[race].columns)):
                rename_cols[name] = race + ' Pop' + name[-3:]
            datasets[race].rename(columns=rename_cols, inplace=True)
            
            # Fix dtypes
            for col in rename_cols.values():
                datasets[race][col] = datasets[race][col].str.replace(',', '').astype('int64')
                
            merge_keys = ['GeoID'] + list(rename_cols.values())
            merged_census = pd.merge(merged_census, datasets[race][merge_keys], on = "GeoID", how = "left")
            
        merged_census.set_index('GeoID', inplace = True)
    except:
        raise Exception('An invalid dataset with vital columns missing was provided, please provide a valid (unprocessed) Census dataset!')
    
    return merged_census
    
def preprocess_datasets(datasets):
    '''
    '''
    census_keys = ['All', 'Asian', 'Black', 'Hispanic', 'White']
    new_datasets = {}
    if 'Drug_Crime' in datasets:
        new_datasets['Drug_Crime'] = preprocess_drug_crime(datasets['Drug_Crime'])

    census_datasets = {}
    for x in datasets:
        if x in census_keys:
            census_datasets[x] = datasets[x]

    new_datasets['Census'] = preprocess_census(census_datasets)
    
    return new_datasets
        