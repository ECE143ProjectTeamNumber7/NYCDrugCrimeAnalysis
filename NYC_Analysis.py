import preprocess_utils as pu
import data_utils as du

def main():
    datasets = pu.import_data()
    datasets = pu.preprocess_datasets(datasets)
    print(du.count_keywords(datasets['Drug_Crime']['Crime'], keywords=['marijuana', 'controlled', 'meth', 'inject', 'prescription', 'paraphernalia']))
    # print(datasets['Drug_Crime'])

if __name__ == '__main__':
    main()