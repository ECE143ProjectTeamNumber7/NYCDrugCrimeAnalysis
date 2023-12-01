import pandas as pd
import numpy as np
import datetime
import nltk
import glob
import os
import re
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

def import_data(filenames = []):
    '''
    Imports datasets of all given filenames. 
    If filenames is empty, this will import all relevant dataset CSVs instead, i.e. Drug_Crime, and all 5 CSVs of 2020_Census/.
    
    Parameters:
        filenames (list):   Optional. List of CSV file names as strings. It is assumed that the filenames will be relative to the current directory.
                            If left empty or an empty list is passed in, it will import all relevant dataset CSVs located in data/
    
    Returns:
        list of datasets as a list tuple where datasets[0] is the file basename and datasets[1] is the pandas dataframe.
    '''
    assert isinstance(filenames, list)

    if len(filenames) == 0:
        filenames = [os.getcwd() + '/data/Drug_Crime_20231111.csv']
        filenames += glob.glob(os.getcwd() + '/data/2020_Census/*.csv')

    # Open and store the datasets
    datasets = {}
    for filename in filenames:
        assert isinstance(filename, str)
        assert '.csv' in filename

        df = pd.read_csv(filename)
        
        # Shorten dataset file name iif is one of the main relevant datasets, otherwise leave label as is
        label_loc = filename.find('Total-Population-')
        if 'Drug_Crime' in filename:
            datasets['Drug_Crime'] = df
        elif label_loc != -1:
            datasets[filename[label_loc + len('Total-Population-'):-4]] = df

    return datasets

def count_time_part(time_col, times = {'hour': 0, 'minute': 0, 'second': 0}):
    '''
    Provides a count dict (similar to value_counts) of the provided individual relevant parts of the time column.

    Parameters:
        time_col (pd.Series):   Column of datatime.time objects to parse through
        times (dict|list|int):  Optional. Dictonary, list, or integer containing the desired part of the time. 
                                As a dict object, the start time can be set as well for the desired part of the time, i.e. `{'hour': 2}`. This is the equivalent to rotating the time set. Default is 0.
                                
                                Allowed input values are `['hour', 'minute', 'second']`
                                Setting start time should wrap around, i.e. 60 -> 0, 24 -> 0
    
    Returns:
        dict of dct of counts. Keys will match the desired part provided in `times`. 
        Each item is a dictonary of every time value and their counts, with the first element being the start time set by times.
    '''
    assert isinstance(time_col, pd.Series)
    assert isinstance(times, dict) or isinstance(times, list) or isinstance(times, str)

    # Set time_components and transform times paremeter to a dict if needed
    time_components = {'hour': {}, 'minute': {}, 'second': {}}
    if isinstance(times, list):
        times = {t: 0 for t in times}
    elif isinstance(times, str):
        times = {times: 0}

    for t in times:
        assert t in time_components.keys()
        assert 0 <= times[t] <= (24 if t == 'hour' else 60)

    for comp in time_components:
        start = 0
        time_cap = 24 if comp == 'hour' else 60
        if comp in times:
            start = times[comp]

        time_components[comp] = {t % time_cap: 0 for t in range(start, time_cap + start)}

    for time_item in time_col:
        assert isinstance(time_item, datetime.time)
        for t in times:
            time_part = getattr(time_item, t)
            time_components[t][time_part] += 1

    return {comp: time_components[comp] for comp in time_components if comp in times}

def group_count_parks(parks):
    '''
    Counts the number of reported instance on each type of park. Performs count on the occurence of the word in the park name.

    Parameter:
        parks (pd.Series):  Column of str with the park names.

    Returns:
        dict of counts. Each key is one of the most common words used in the park names.
    '''
    assert isinstance(parks, pd.Series)

    nltk.download('punkt')
    all_text = ' '.join(parks.unique())

    locs = word_tokenize(all_text.lower())  # Convert to lowercase for case-insensitivity

    top_locs = FreqDist(locs).most_common(15)
    park_loc_count = parks.value_counts().to_dict()
    freq_loc_count = {word[0]: 0 for word in top_locs}

    # Count of each most frequent word that was in a park name
    for loc in park_loc_count:
        assert isinstance(loc, str)
        for freq_loc in freq_loc_count:
            if freq_loc in loc.lower():
                freq_loc_count[freq_loc] += park_loc_count[loc]

    freq_loc_count.pop("'s")
    freq_loc_count.pop('on')
    freq_loc_count.pop('st.')
    freq_loc_count.pop('avenue')
    freq_loc_count.pop('south')
    freq_loc_count.pop('street')

    return freq_loc_count

def filter_by_boro_feature(dataset, boro = '', feature = '', rename = True):
    '''
    Filterest the dataset by the inputed borough and feature. Filter designed for the preprocessed Census dataset column and rows.

    Parameters:
        dataset (pd.DataFrame): Complete dataframe of the dataset. 
        boro (str):             Optional. The desired borough to fliter by. If empty (default), all boroughs returned.
        feature (str):          Optonal. The desired feature to filter by. If empty (default), all features returned.
        rename (bool):          Optional. Whether to rename the feature column. This renames the column to only the identifier if column had prepended identifiers, e.g. "All Pop_10" -> "All". Defaults to `True`.
    
    Returns:
        pd.DataFrame with the filtered boroughs and features.
    '''
    assert isinstance(dataset, pd.DataFrame) and isinstance(boro, str) and isinstance(feature, str) and isinstance(rename, bool)

    feature_list = ['Pop Change', 'Natural Change', 'Net Migration', 'Pop_10', 'Pop_20']
    assert feature in feature_list
    
    # Create deep copy of filtered dataset to not affect orignal and filter for the desired feature
    filtered_dataset = dataset.copy(deep=True) if boro == '' else dataset.loc[dataset['Borough'] == boro] 
    population_col_filter = re.compile(f'.*{feature}')
    filtered_cols = list(filter(population_col_filter.match, dataset.columns))
    filtered_dataset = filtered_dataset[filtered_cols]
    
    # Rename column to only their identifier if features was filtered
    if feature != '' and rename:
        rename_cols = {}
        for col in filtered_cols:
            rename_cols[col] = col[:col.find(' ')]
        filtered_dataset.rename(columns=rename_cols, inplace=True)
    
    return filtered_dataset

def normalize(dataset, axis='row', inplace=False):
    '''
    Normalizes the provided dataset along the row or column axis of the table using Numpy's euclidean unit vector normalization.

    Parameters:
        dataset (pd.DataFrame): Complete dataframe of the dataset to be normalized.
        axis (str):             Optional. Specify `'row'` or `'col'` axis to be normalized. Defaults to `'row'`.
        inplace (bool):         Optional. Normalize the dataset inplace without creating a deep copy. Defaults to `False`.

    Returns:
        pd.DataFrame of the normalized dataset.
    '''
    assert isinstance(dataset, pd.DataFrame) and isinstance(axis, str) and isinstance(inplace, bool)
    assert axis in ['row', 'col']

    norm_dataset = dataset.copy(deep=inplace)
    
    if axis == 'row':
        for row in norm_dataset.index:
            row_vals = norm_dataset.loc[row].to_numpy()
            norm_dataset[row:row] = row_vals / np.linalg.norm(row_vals, axis=0)
    else:
        for col in norm_dataset.columns:
            col_vals = norm_dataset.loc[:, col]
            norm_dataset[col] = col_vals / np.linalg.norm(col_vals, axis=0)
        
    return norm_dataset