import preprocess_utils as pu

def main():
    datasets = pu.import_data()
    datasets = pu.preprocess_datasets(datasets)

if __name__ == '__main__':
    main()