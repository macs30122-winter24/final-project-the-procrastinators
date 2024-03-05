### A Brief Introduction

Rural hospitals in the United States are closing at an alarming -- and increasing -- rate. These closures have a variety of negative impacts on surrounding communities, diminishing access to medical care and removing a vital economic hub. 

Multiple aspects of rural hospital closures are currently understudied or unknown. First, many studies assume that rural hospitals either fully close or remain open, without leaving room for any middle options. Nonetheless, rural hospital failures do not necessarily have to result in a full closure but can also result in conversions (also called partial closures) in which the facility is turned into a smaller variety of medical facility, such as an urgent care or nursing facility. Facility conversion could provide an avenue for failing hospitals to continue providing some services to their community, which may dampen the impact of a closure. 

Secondly, although rural hospital closures increase outmigration pressure and decrease the desirability of an area for inmigration, it's not known whether rural hospital closures have any real change on migration trends into a county. Such trends are relevant from a policy and social point of view. If communities are outmigrating in response to hospital closures, for instance, then there is the potential for hospital closures to cause an increased breakdown of rural communities. If communities "stay put" in response to hospital closures, then there is a potential for an increase in urban/rural health gaps. 

Lastly, given the increasing rate of rural hospital closures, predicting rural hospital closures could prove fruitful to help prevent closures from occurring in the first place, although litle work has been done in this area.

Towards addressing these issues, we proposed and addressed two research questions for this project:

1. To what extent do rural hospital closures and conversions impact migration trends in their surrounding counties?

2. To what extent can rural hospital closures be predicted using data about the hospital and its surrounding county?

We address the first research question through the usage of a difference-in-difference design, and find that rural hospital closures and conversion have little to no impact on migration behavior in their home county. This indicates that rural populations tend to "stay in place," in light of closures, a finding which redoubles the need for increased provision of medical care to rural communities suffering hospital closures.

We address the second research question through the use of statistical and machine learning methods. First, we use logistic regression to determine if hospital index, county index, or rurality index is significant that explain the closure of hospital. We find that  FarP, Ruca Rural Percentage, Total Medicare Days, Total Days, and Median Income are significant estimator at 80% confidence level. Furthermore, we also test different machine learning methods. The naive bayesian and random forest method does not work well for the imbalanced dataset we have.

Next, we use machine learning models to identify the top predictors for hospital closure. We find that both hospital features and county features can be used to classify hospitals with over 80% accuracy. Rurality is found to be a good predictor for closure, along with AGI outflow, suggesting that hospitals in poorer and more rural counties are more likely to close.

### Repository Overview

Our top-level folders contain the following:

* `notebooks`: contains all analysis notebooks

* `scripts`: contains all scripts used to acquire, wrangle, and transform our datasets.

* `data`: contains all datasets created for or by our analysis. The `raw` subfolder contains raw data downloaded from our data sources, while `shapes` contains spatial data. Datasets outside of any subfolders were intermediate products of our data aggregation process.

* `results`: contains our project presentations (both [old](https://github.com/macs30122-winter24/final-project-the-procrastinators/blob/main/results/Final%20Presentation%20(Original).pdf) and [revised](https://github.com/macs30122-winter24/final-project-the-procrastinators/blob/main/results/Final%20Presentation%20(Edited).pdf)) and progress report.

We exclusively used Python scripts for data wrangling to increase computational reproducibility.

#### Data Sources

* **American Community Survey**: used for county level characteristics, pulled using the Census' [American Community Survey APIs](https://www.census.gov/programs-surveys/acs/data/data-via-api.html).

* **IRS**: we retrieved their annual [migration data](https://www.irs.gov/statistics/soi-tax-stats-migration-data) 

* **Center for Medicare and Medicaid Service Cost reports**: we used specifically the [Hospitals 2552-2010 form](https://www.cms.gov/data-research/statistics-trends-and-reports/cost-reports/hospital-2552-2010-form), performing heavy record linkage on the forms to massage the data into a workable format. 

* **Sheps Center**: The Cecil G. Sheps Center for Health Services Research tracks rural hospital closures and conversions; we [used their list for our analysis](https://www.shepscenter.unc.edu/programs-projects/rural-health/rural-hospital-closures/).

* **USDA ERS**: we used two of their rural classifications -- the [Frontier and Remote Area](https://www.ers.usda.gov/data-products/frontier-and-remote-area-codes/) codes and [Rural Urban Commuting Areas](https://www.ers.usda.gov/data-products/rural-urban-commuting-area-codes/) codes

* **CDC**: we used the [CDC's Urban-Rural Classification Codes](https://www.cdc.gov/nchs/data_access/urban_rural.htm)

* **Housing and Urban Development**: The US Department of Housing and Urban Development publishes quarterly [ZIP-County crosswalk files](https://www.huduser.gov/portal/datasets/usps_crosswalk.html), one of which we retrieved to process the Frontier and Remote Area codes.

* **Google Maps API Geocoder**: used to geocode hospitals; documentation available [here](https://developers.google.com/maps/documentation).

#### Dependencies

Required dependencies can be found in `requirements.txt`.

### Running the Code

1. Download hospital data from ... and then run ...  <@ ASHLYNN>

2. Download IRS data from ... and then run ... <@ XUZHOU>

3. Download ACS data with `GetCensusData.py`. Run `MergeData.py` to combine with IRS data, and then `JoinData.py` to combine with hospital data.

4. Modelling and data analysis can be replicated within `MigrationAnalysis.ipynb`, `Regression.ipynb` and `Modelling.ipynb`.

 
### Division of Labor

Ashlynn Wimer:
* Wrote the following scripts:
  * `CleanHospitals.py`: Script that performs a record linkage across our (shockingly messy) hospital datasets to create a hospital table.
  * `GenerateRuralityTables.py`: Script which creates county level rurality indicators based upon the tract and zip level USDA ERS county level indicators, before merging them with the CDC Rurality indicators.
  * `GeocodeHospitals.py`: Script which geocodes the hospitals from the `CleanHospitals` script
  * `GetShapes.py`: Script which acquires county shapefiles.
  * `GoogleAPIBuddy.py`: Small wrapper class for interacting with Google's geocoding API.
* Analyzed the impact of hospital closures and conversions on migration (`MigrationAnalysis.ipynb`)
* Created initial project proposal
* Created majority of `readme.md`
* Added descriptions of relevant datasources to project in the progress report.
* Slides for own portions of project (including quick generation of of a reference map through `ReferenceMapMaker.ipynb`)

Dan Gilles:
* Wrote the following scripts:
  * `GetCensusData.py`: Acquires ACS1, ACS5 and ACSSE data on population, income and unemployment from the years 2011-2022 from the Census API
  * `GetCensusVars.py`: Saves the census variables and their explanations to a CSV file
  * `MergeData.py`: Gets the data from the IRS, Census Bureau and Rurality and merges it into a full census-level dataset
  * `JoinData.py`: Joins the census-level dataset with the hospital dataset to create our final dataset for analysis
* Visualized and created models to determine the differences between closed and unclosed hospitals (`Modelling.ipynb`)
* Slides for own portions of project 

Xuzhou Ding:
* Wrote the following scripts:
  * `IRS_Data.py`: Script that performs creation of IRS data in the file for both inflow and outflow. It records the Inflow and outflow of estimated Individual, Household, Net AGI in each county.
  * `Regression.ipynb`: Jupyter Notebook that covers modification of dataset, logistic regression, naive bayesian classifier, and random forest classifier.
* Slides for own portions of project 
