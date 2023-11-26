import preprocess_utils as pu
import data_utils as du

def main():
    datasets = pu.import_data()
    datasets = pu.preprocess_datasets(datasets)
    # print(du.count_keywords(datasets['Drug_Crime']['Crime'], keywords=['marijuana', 'controlled', 'meth', 'inject', 'prescription', 'paraphernalia']))
    # print(du.count_keywords(datasets['Drug_Crime']['Crime'], keywords=['sale', 'poss', 'loit', 'influence']))
    # print(datasets['Drug_Crime'])
    # # print(datasets['Drug_Crime']['Time of Day'].value_counts())
    # print(du.group_count_parks(datasets['Drug_Crime']['PARKS_NM']))
    # print(datasets['Drug_Crime']['Precinct'])
    # print(du.precincts(datasets['Drug_Crime']['Precinct']))
    
    print(du.filter_by_boro_feature(datasets['Census'], feature='Pop_10').dtypes)
#     boro = 'Manhattan'
# datasets['Census'].loc[datasets['Census']['Borough'] == boro]

if __name__ == '__main__':
    main()