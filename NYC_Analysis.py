import preprocess_utils as pu

def preprocess_datasets(datasets):
    datasets['Drug_Crime']['PARKS_NM'] = pu.replace_column_nan(datasets["Drug_Crime"]['PARKS_NM'], oldnan='(null)').fillna('Not at a park')
    
    new_columns = {'CMPLNT_NUM': 'ID', 'CMPLNT_FR_DT': 'Year', 'CMPLNT_FR_TM': 'Time', 'CMPLNT_TO_DT': 'EndYear', 
                        'RPT_DT': 'Reported on:', 'ADDR_PCT_CD': 'Precinct', 'KY_CD': 'Offense_Code',
                        'OFNS_DESC': 'Description', 'CRM_ATTP_CPTD_CD': 'Completed?'}
    datasets['Drug_Crime'].rename(columns=new_columns, inplace=True)
    
    datasets['Drug_Crime'].drop(columns = ['CMPLNT_TO_TM', 'Latitude', 'Longitude'], inplace = True)
    
    pu.isolate_date_part(datasets['Drug_Crime'], ['Year', 'Reported on:', 'EndYear'], 'y')
    
    datasets['Drug_Crime'].set_index('ID', inplace = True)
    
    # TODO: Isolate Drug Crime Possession Type
    pd_desc_mapping = {'CONTROLLED SUBSTANCE,POSSESS.', 'CONTROLLED SUBSTANCE, POSSESSI' }
    
    return datasets

def main():
    datasets = pu.import_data()
    datasets = preprocess_datasets(datasets)
    print(datasets['Drug_Crime'])

if __name__ == '__main__':
    main()