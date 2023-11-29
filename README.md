# NYCDrugCrimeAnalysis

### File Structure
```
+-- data
|   +-- Drug_Crime_20231111.csv
|   +-- 2020_Census
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Asian.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Black.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-Hispanic.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population-White.csv
|   |   +-- dcp-comps-of-chg-StoryMap-data-032023-Total-Population.csv
+-- utils.py
+-- NYC_Analysis.py
```

### Modules
* [OS](https://docs.python.org/3/library/os.html)
* [Glob](https://docs.python.org/3/library/glob.html)
* [Pandas](https://pandas.pydata.org/docs/reference/index.html)
* [NumPy](https://numpy.org/doc/stable/reference/index.html#reference)
* [Matplotlib/Plotly]

### How To Use
1. **Install Necessary Modules**
The modules listed above are used to run the visualizations. Installing [Anaconda](https://www.anaconda.com/) is suggested; however, only those are required at minimum and can be installed with `pip`. Having the same version is crucial; some visualizations utlize features from more recent versioins.
2. 

### Proposal
As you are aware, drug-related crimes have been a persistent issue in urban areas,
including New York City. Understanding the dynamics and patterns of these crimes can have
significant implications for law enforcement and policymakers. Research in this field can
provide insights into the underlying factors of drug-related crimes in NYC.

Our project proposal aims to explore the trends and patterns in drug crimes in NYC using
available data that includes the precincts where these crimes occurred, the specific time of when
they occured, when the crime was reported, descriptions and levels of offense, whether the
crime was successfully completed, latitude-longitude coordinates, and more.

Also, we will investigate the correlation between the crimes and other factors, like
geography, population, race, and compare the difference between districts. We aim to identify
geographical hotspots and coldspots of drug-related crimes within NYC, using provided data that
includes lat-lon coordinates. We will examine temporal patterns to understand when drug-related
crimes are more likely to occur during the day, which can shed light on potential contributing
factors. We intend to categorize drug-related offenses by type and severity, offering a deeper
understanding of the nature of these crimes in the city.

Our project will involve data cleaning and preprocessing to ensure data quality and
accuracy. Multiple columns/features in the dataset have NaNs or ambiguous values (precinct #),
and we will deal with this appropriately. We will use various data analysis techniques, including
spatial analysis, time series analysis, and data visualization, to achieve the project’s objectives.

### Relevant Datasets/Data
Drug Crime | NYC Open Data (cityofnewyork.us)
BYTES of the BIG APPLE - DCP (nyc.gov)
2020 Census -DCP (nyc.gov)

#### Plan
| Task | Estimated Time | People Involved |
| ---- | ---- | ---- |
| Extracting Data and Merging Into 1 Dataset | 1.5 weeks | Stephen Dong, Ali Hussain, Kavinder Kanthen, Kai Lu. |
| Cleaning/Preprocessing | 1.5 weeks | Ali Hussain, Kai Lu, Bill (Xuehai Yan) |
| Data Visualization | 1 week | Kavinder Kanthen, Bill (Xuehai Yan), Stephen Dong |