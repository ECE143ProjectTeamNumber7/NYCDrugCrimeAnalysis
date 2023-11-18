import pandas as pd
import numpy as np
import glob
import os

def import_data(filenames = []):
    """
    Imports datasets of all given filenames. 
    If filenames is empty, this will import all relevant dataset CSVs instead, i.e. Drug_Crime, and all 5 CSVs of 2020_Census/.
    
    Parameters:
        filenames (list):   Optional. List of CSV file names as strings. It is assumed that the filenames will be relative to the current directory.
                            If left empty or an empty list is passed in, it will import all relevant dataset CSVs located in data/
    
    Returns:
        List of datasets as a tuple where datasets[0] is the file basename and datasets[1] is the pandas dataframe.
    """
    assert isinstance(filenames, list)

    if len(filenames) == 0:
        filenames = [os.getcwd() + '/data/Drug_Crime_20231111.csv']
        filenames += glob.glob(os.getcwd() + '/data/2020_Census/*.csv')

    datasets = []
    for filename in filenames:
        assert isinstance(filename, str)
        assert ".csv" in filename

        df = pd.read_csv(filename)
        datasets.append((os.path.basename(filename), df))

    return datasets

def fix_column_nan(column, datatype):
    """
    Fixes the column's NaN values to match the given datatype. New column is returned.
    Useful for fixing the NaN values to match or be compatible for modifcations of the column's dtype.
    e.g. Convertng date str dtype to DateTime dtype requires any potential NaN, i.e. empty entry treated as a `float64` dtype, to be converted to `str` first.

    Generally, fixing only occurs between 2 types (`float64` <=> `str`) as Python will do the rest of the work.

    Parameters:
        column (Series):    Column series from dataframe of which the NaN values should be fixed.
        datatype (str):     Datatype each NaN value in the column should be converted into.

    Returns:
        Newly converted column Series.
    """
    pass

def replace_col_nan_values(column, key = {}):
    """
    Replaces all column NaN values with a specified human readable value. New column is returned.
    Useful for data visualzation or table exporting of which NaN values such as `np.nan` or `None` will be represented as empty or in an ugly format.
    e.g. Converting `np.nan` to "no response"

    Parameters:
        column (Series):    Column series from dataframe of which the NaN values should be replaced.
        key (dict):         Optional. Dictionary of NaN representation values as the key and the human readable format as the value.
                            If `key` is left empty, `np.nan` and `None` values are replaced with "none"

    Returns:
        Newly converted column Series.
    """
    pass

def convert_data(data, conv_table = {}):
    """
    Converts the data type of the respective column in the dataframe to the corresponding datatype, inplace. Original dataframe will be returned.
    Useful for when a column of the pandas dataframe is a `str` object, but should or can be converted to an actual Python datatype.
    e.g. Converting 08/27/2001 `str` object to `DateTime` object.

    Parameters:
        data (pd.DataFrame):    Dataframe of which the columns shall be modified.
        conv_table (dict):      Optional. Dictionary off column names as the key and datatype as the value
    
    Returns:
        Original pandas dataframe to be used for reference or discarded.
    """
    pass
