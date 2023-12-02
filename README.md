# NYCDrugCrimeAnalysis

### File Structure
```
+-- data
|   +-- Drug_Crime_20231111.csv
|   +-- 2020_Census/
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Asian.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Black.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Hispanic.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-White.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population.csv
|   +-- City_Features/
|   |   +-- Borough_Boundaries.geojson
|   |   +-- Community_Districts.geojson
|   +-- Housing_Prices/
|   |   +-- 2015_bronx.xls
|   |   +-- 2015_brooklyn.xls
|   |   +-- 2015_manhattan.xls
|   |   +-- 2015_queens.xls
|   |   +-- 2015_statenisland.xls
|   +-- Race Pie Chart/
|   +-- nyc_population_2010_2020_change-core-geographies.xlsx
|   +-- Population_by_District.xlsx
+-- data_utils.py
+-- preprocess_utils.py
+-- NYC_Drug_Crime_Visualizations.ipynb
+-- NYC_Drug_Crime_Visualizations.html
+-- ECE143_Team7_Presentation.pdf
```
* `data` stores all datasets for analysis.
    * `Drug_Crime_20231111.csv` is the primary dataset that stores all NYC drug crime data points.
    * `2020_Census` stores all NYC Census data (manually reformatted and split by race).
    * `City_Features` stores all NYC district and borough `geojson` format datasets for geographical analysis via Folium.
    * `Housing_Prices` stores all NYC housing prices datasets by borough.
    * `Race Pie Chart` stores all generated Pie Charts generated by the Visualization Notebook. This is technically a runtime directory, but data is kept for individual analysis of the racial compositions outside of the notebook.
    * `nyc_population_2010_2020_change-core-geographies.xlsx` is a secondary dataset similar to `2020_Census` with additional `GeoID` information.
    * `Population_by_District.xlsx` is the manually preprocessed dataset of `nyc_population_2010_2020_change-core-geographies.xlsx`
* `data_utils.py` contains supplementary minimally specific functions to quick access and perform certain dataset related functionalities. Many functions expect the data provided to be preprocessed.
* `preprocess_utils.py` contains all preprocessing functions used to preprocess the primary datasets (`Drug_Crime` and `2020_Census`).
* `NYC_Drug_Crime_Visualizations.ipynb` is our visualization notebook
* `NYC_Drug_Crime_Visualizations.html` is the html version of our html notebook. This is provided as some visualizations will not render correctly when viewed or downloaded on GitHub.
* `ECE143_Team7_Presentation.pdf` is the pdf of our presentation.

### Modules
**Files**
* [os](https://docs.python.org/3/library/os.html)
* [glob](https://docs.python.org/3/library/glob.html)
* [json](https://docs.python.org/3/library/json.html)

**Data Manipulation**
* [pandas](https://pandas.pydata.org/docs/reference/index.html)
* [numpy](https://numpy.org/doc/stable/reference/index.html#reference)
* [statistics](https://docs.python.org/3/library/statistics.html)

**Visualization**
* [matplotlib](https://matplotlib.org/stable/users/index)
* [plotly](https://plotly.com/python-api-reference/)
* [seaborn](https://seaborn.pydata.org/api.html)
* [folium](https://python-visualization.github.io/folium/latest/user_guide.html)
* [shapely](https://shapely.readthedocs.io/en/stable/manual.html)

### How To Use
* **Downloading this Repository**
    * Clone the repository:
        - via ssh: `git clone git@github.com:ECE143ProjectTeamNumber7/NYCDrugCrimeAnalysis.git`
        - via html: `git clone https://github.com/ECE143ProjectTeamNumber7/NYCDrugCrimeAnalysis.git`
    * **Note:** `Drug_Crime_20231111.csv` is a large file. Check in `data/` if the csv was cloned. If it is missing, you will need to perform a `git lfs pull`.

* **Install Necessary Modules**
The modules listed above are used to run the visualizations. Installing [Anaconda](https://www.anaconda.com/) is suggested; however, only the ones listed above are required at minimum and can be installed with `pip`. Note that some modules, such as *folium* or *shapely*, may not be included with anaconda and will require seperate installation with `pip`. In the Notebook, some functions require dependencies that may not be included in Anaconda and may vary across machines; thus, it is vital you pay careful attention to possible errors raised by missing dependencies. Having the same version is crucial; some visualizations utlize features from more recent versioins.

* **Running Our Visualizations** 
Open `NYC_Drug_Crime_Visualizations.ipynb` in `VSCode` or via `jupyter notebook` in a terminal with anaconda. Press `>> Run all` to run all visualization code. Everything used to run and analyze the datasets are included in the notebook.

#### Self Analysis
If you would like to perform your own analysis with our datasets, here is a guide to run the codes:
1. **Importing Primary Datasets:**
    ```Python
    import data_utils as du

    #### Read in the raw dataset. 
    # import_csv_data() will return a dict with the filename as the key and the dataset as a pd.DataFrame as the value.
    # Leaving it blank like below will import all relevant datasets (Drug_Crime and 2020_Census/) and also rename them to a simplified form. 
    # Note: If you have other .csv datasets, their keys *will not* be renamed.
    # This line will store {'Drug_Crme': {...}, 'All': {...}, 'Asian': {...}, 'White': {...}, ...}
    # Indices are: ['All', 'Asian', 'Black', 'Hispanic', 'White']
    raw_datasets = du.import_csv_data()
    ```

2. **Preprocessing**
    - There are two ways to preprocess: quick preprocessing and manual preprocessing. Quick preprocessing is recommended and a guide ise provided below; however, manual preprocessing is allowed by manually calling the individual preprocessng steps in `preprocessing_utils`.
    - *Quick Preprocessing:*
        * In this case, quick preprocessing does not mean it is fast at its job, but rather preprocessing is done at the "press of a button". The datasets are large, so preprocessing takes some time.
        ```Python
        #### Preprocess the raw dataset.
        # preprocess_datasets() will automatically perform all preprocessing on the primary datasets (Drug_Crime, 2020_Census).
        # The dict with each of the datasets should must be provded for any preprocessing to occur. 
        # However, the dict is not required to be filled or complete with all the raw_datasets; although, it is better to do so in order to preprocess all at once.
        # Only datasets in the dict with keys belong in ['Drug_Crime', 'All', 'Asian', 'Black', 'Hispanic', 'White'] will be preprocessed.
        # Moreover, the provided census datasets will be merged into one dataset.
        # This line will store {'Drug_Crime': {...}, 'Census': {...}}
        # Indices are: ['Drug_Crime', 'Census']
        datasets = pu.preprocess_datasets(raw_datasets)
        ```
    - *Additional Preprocessing:*
        * Additional preprocessng can be done on the dataset after quick preprocessing. Two that were performed on our dataset are provided. The decision to not include these steps in the quick preprocessing is ther capability for other uses. For example, the missing data in the years and be filled via machine learning using the existing data given an extremely good model. And the unknown boroughs may also be desired depending on the visualization or analytical uses, such as looking into if the lack of borough info can be associate with some cause.
            ```Python
            # Drop all rows before 2006 due to lack of sufficient data as shown in visualization
            datasets['Drug_Crime'] = datasets['Drug_Crime'].drop(datasets['Drug_Crime'][datasets['Drug_Crime']['Year'] < 2006].index)
            ```
            
            ```Python
            # Clean missing boroughs and drop any un-associated data values
            datasets['Drug_Crime'] = pu.clean_missing_boroughs(datasets['Drug_Crime'])
            ```
        * This uses the folowing functon in `preprocessing_utils`:
            `def clean_missing_boroughs(dataset, validity_threshold = 0.2)`
            Dataset by associating missing borough data with ther precinct numbers and dropping remaining unknown boroughs. `validity_threshold` can be used to specify a specific threshold to which a precinct number can be allowed assocated with a borough. Lower threshold $\Rightarrow$ more valid precinct numbers.

            > Parameters: 
            - dataset : pd.DataFrame
            - validity_threshold : float

            > Returns: 
            - pd.DataFrame drug crime dataframe with modified borough name column.

            > Example:
            - Cleans `Drug_Crime` dataset of missing borough values.
               ```Python
               datasets['Drug_Crime'] = pu.clean_missing_boroughs(datasets['Drug_Crime'])
               ```

3. **Data Processing**
Data manipulation is expected to be manual, but some semi-generalized functions are provided to help simplify the process in `data_utils` (suggested import convention: `import data_utils as du`):

    * `def count_time_part(time_col, times = {'hour': 0, 'minute': 0, 'second': 0})`
    Provides a count dict (similar to value_counts) of the provided individual relevant parts of the time column.
        > Parameters:
            
        - time_col : pd.Series   
            Column of datatime.time objects to parse through
        - times : dict, list, int  
            Optional. Dictonary, list, or integer containing the desired part of the time. 
            As a dict object, the start time can be set as well for the desired part of the time, i.e. `{'hour': 2}`. This is the equivalent to rotating the time set. Default is 0. Allowed input values are `['hour', 'minute', 'second']`. Setting start time should wrap around, i.e. 60 -> 0, 24 -> 0.
        
        > Returns:
        - dict of dict of counts. Keys will be the desired part provided in `times`. 
            Each item is a dictonary of every time value and their counts, with the first element being the start time set by times.

        > Example:
        - Getting a count of each hour from 0 to 23, where result dictionary is sorted to start at hour 5.
            ```Python
            # datasets['Drug_Crime']['Time'] is a column
            >>> du.count_time_part(datasets['Drug_Crime']['Time'], times={'hour': 5})['hour']
            {5: 2436, 6: 5793, 7: 3215, 8: 4760, 9: 6801, 10: 8256, 11: 11910, 
            12: 16966, 13: 21710, 14: 24486, 15: 25085, 16: 28492, 17: 28840, 
            18: 30384, 19: 35957, 20: 35824, 21: 34066, 22: 32063, 23: 26056, 
            0: 22272, 1: 17901, 2: 10131, 3: 6318, 4: 3768}
            ```
    <br>

    * `def group_count_parks(parks)`
    Counts the number of reported instance on each type of park. Performs count on the occurence of the word in the park name.

        > Parameter:
        - parks : pd.Series  
            Column of str with the park names.

        > Returns:
        - dict of counts. Each key is one of the most common words used in the park names.

        > Example:
        - Get a count of each park type in the `PARKS_NM` column.
            ```Python
            # datasets['Drug_Crime']['PARKS_NM'] is a column
            >>> du.group_count_parks(datasets['Drug_Crime']['PARKS_NM'])
            {'park': 442269, 'playground': 654, 'unnamed': 38, 'square': 548, 'bronx': 189, 
            'garden': 17, 'river': 286, 'parkway': 83, 'beach': 235}
            ```
    <br>

    * `def filter_by_boro_feature(dataset, boro = '', feature = '', rename = True)`
    Filterest the dataset by the inputed borough and feature. Filter designed for the preprocessed Census dataset column and rows.

        > Parameters:
        - dataset : pd.DataFrame
            Complete dataframe of the dataset. 
        - boro : str
            Optional. The desired borough to fliter by. If empty (default), all - boroughs returned.
        - feature : str
            Optonal. The desired feature to filter by. If empty (default), all - features returned.
        - rename : bool
            Optional. Whether to rename the feature column. This renames the column to only the identifier if column had prepended identifiers, e.g. "All Pop_10" $\rightarrow$ "All". Defaults to `True`.
        
        > Returns:
        - pd.DataFrame with the filtered boroughs and features.

        > Example:
        - Filter the dataset by the boroughs (total sum) on the `Pop_10` feature.
            ```Python
            # datasets['Drug_Crime']['PARKS_NM'] is a column
            >>> total_census = datasets['Census'].iloc[:][0:6].set_index('Borough', drop=False)
            >>> du.filter_by_boro_feature(total_census, feature='Pop_10')
                            All         Asian       Black       Hispanic       White
            Borough 					
            New York City     8242624     1028119     1861295     2336076        2722904
            Manhattan         1585873     177624      205340      403577         761493
            Bronx             1385108     47335       416695      741413         151209
            Brooklyn          2504700     260129      799066      496285         893306
            Queens            2230722     508334      395881      613750         616727
            Staten Island     468730      34697       44313       81051          300169
            ```
    <br>

    * `def normalize(dataset, axis='row', inplace=False)`
    Normalizes the provided dataset along the row or column axis of the table using Numpy's euclidean unit vector normalization.

        > Parameters:
        - dataset : pd.DataFrame
            Complete dataframe of the dataset to be normalized.
        - axis : str     
            Optional. Specify `'row'` or `'col'` axis to be normalized. Defaults to `'row'`.
        - inplace : bool
            Optional. Normalize the dataset inplace without creating a deep copy. Defaults to `False`.

        > Returns:
        - pd.DataFrame of the normalized dataset.

        > Example:
        - Normalized the filtered borough dataframe `filtered_race_10`.
            ```Python
            # datasets['Drug_Crime']['PARKS_NM'] is a column
            >>> du.normalize(filtered_race_10)
                            All          Asian        Black        Hispanic 
            Borough 				
            New York City     0.246523     0.446302     0.560146     0.652899
            Manhattan         0.196578     0.227251     0.446641     0.842749
            Bronx             0.054715     0.481661     0.857006     0.174784
            Brooklyn          0.196613     0.603956     0.375106     0.675186
            Queens            0.469520     0.365654     0.566887     0.569637
            Staten Island     0.109810     0.140244     0.256513     0.949986
            ```

### Proposal
As you are aware, drug-related crimes have been a persistent issue in urban areas, including New York City. Understanding the dynamics and patterns of these crimes can have significant implications for law enforcement and policymakers. Research in this field can provide insights into the underlying factors of drug-related crimes in NYC.

Our project proposal aims to explore the trends and patterns in drug crimes in NYC using available data that includes the precincts where these crimes occurred, the specific time of when they occured, when the crime was reported, descriptions and levels of offense, whether the crime was successfully completed, latitude-longitude coordinates, and more.

Also, we will investigate the correlation between the crimes and other factors, like geography, population, race, and compare the difference between districts. We aim to identify geographical hotspots and coldspots of drug-related crimes within NYC, using provided data that includes lat-lon coordinates. We will examine temporal patterns to understand when drug-related crimes are more likely to occur during the day, which can shed light on potential contributing factors. We intend to categorize drug-related offenses by type and severity, offering a deeper understanding of the nature of these crimes in the city.

Our project will involve data cleaning and preprocessing to ensure data quality and accuracy. Multiple columns/features in the dataset have NaNs or ambiguous values (precinct #), and we will deal with this appropriately. We will use various data analysis techniques, including spatial analysis, time series analysis, and data visualization, to achieve the project’s objectives.

### Relevant Datasets/Data
* [Drug Crime | NYC Open Data](cityofnewyork.us)  
* [BYTES of the BIG APPLE - DCP](nyc.gov)  
* [2020 Census - DCP](nyc.gov)  
* [Community Districts Geospacial](https://data.cityofnewyork.us/City-Government/Community-Districts/yfnk-k7r4)
* [Borough Boundaries Geospacal](https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm)

#### Plan
| Task | Estimated Time | People Involved |
| ---- | ---- | ---- |
| Extracting Data and Merging Into 1 Dataset | 1.5 weeks | Stephen Dong, Ali Hussain, Kavinder Kanthen, Kai Lu. |
| Cleaning/Preprocessing | 1.5 weeks | Ali Hussain, Kai Lu, Bill (Xuehai Yan) |
| Data Visualization | 1 week | Kavinder Kanthen, Bill (Xuehai Yan), Stephen Dong |
