### A Brief Introduction

Rural hospitals in the United States are closing at an alarming -- and increasing -- rate, with over 140 rural hospitals having closed over from 2011-2021 alone. These closures have a variety of negative impacts on surrounding communities, diminishing access to medical care and removing a vital economic hub. 

Multiple aspects of rural hospital closures are currently understudied or unknown. First, many studies assume that rural hospitals either fully close or remain open, without leaving room for any middle options. Nonetheless, rural hospital failures do not necessarily have to result in a full closure but can also result in conversions (also called partial closures) in which the facility is turned into a smaller variety of medical facility, such as an urgent care or nursing facility. Facility conversion could provide an avenue for failing hospitals to continue providing some services to their community, which may dampen the impact of a closure. 

Secondly, although rural hospital closures increase outmigration pressure and decrease the desirability of an area for inmigration, it's not known whether rural hospital closures have any real change on migration trends into a county. Such trends are relevant from a policy and social point of view. If communities are outmigrating in response to hospital closures, for instance, then there is the potential for hospital closures to cause an increased breakdown of rural communities. If communities "stay put" in response to hospital closures, then there is a potential for an increase in urban/rural health gaps. 

Lastly, given the increasing rate of rural hospital closures, predicting rural hospital closures could prove fruitful to help prevent closures from occurring in the first place, although litle work has been done in this area.

Towards addressing these issues, we proposed and addressed three research questions for this project:

1. To what extent do rural hospital closures and conversions impact migration trends in their surrounding counties?

2. To what extent can rural hospital closures be predicted using data about the hospital and its surrounding county?

We address the first research question through the usage of a difference-in-difference design, and find that rural hospital closures and conversion have little to no impact on migration behavior in their home county. This indicates that rural populations tend to "stay in place," in light of closures, a finding which redoubles the need for increased provision of medical care to rural communities suffering hospital closures.

We address the second research question through <@ DAN AND XUZHOU>

### Repository Overview

Our top-level folders contain the following:

* `notebooks`: contains all analysis notebooks

* `scripts`: contains all scripts used to acquire, wrangle, and transform our datasets.

* `data`: contains all datasets used for, or created by, analysis. The `raw` subfolder contains raw data downloaded from our data sources, while `shapes` contains spatial data. Datasets outside of any subfolders were intermediate products of our data aggregation process.

* `results`: contains our project presentation(s) and progress report.

We exclusively used Python scripts for data wrangling to increase computational reproducibility.

#### Data Sources

* **American Community Survey**: used for county level characteristics, pulled using the Census' [American Community Survey APIs](https://www.census.gov/programs-surveys/acs/data/data-via-api.html).

* **IRS**: we retrieved their annual [migration data](https://www.irs.gov/statistics/soi-tax-stats-migration-data) 

* **Center for Medicare and Medicaid Servicse Cost reports**: we used specifically the [Hospitals 2552-2010 form](https://www.cms.gov/data-research/statistics-trends-and-reports/cost-reports/hospital-2552-2010-form), performing heavy record linkage on the forms to massage the data into a workable format. 

* **Sheps Center**: The Cecil G. Sheps Center for Health Services Research tracks rural hospital closures and conversions; we [used their list for our analysis](https://www.shepscenter.unc.edu/programs-projects/rural-health/rural-hospital-closures/).

* **USDA ERS**: we used two of their rural classifications -- the [Frontier and Remote Area](https://www.ers.usda.gov/data-products/frontier-and-remote-area-codes/) codes and [Rural Urban Commuting Areas](https://www.ers.usda.gov/data-products/rural-urban-commuting-area-codes/) codes

* **CDC**: we used the [CDC's Urban-Rural Classification Codes](https://www.cdc.gov/nchs/data_access/urban_rural.htm)

* **Housing and Urban Development**: The US Department of Housing and Urban Development publishes quarterly [ZIP-County crosswalk files](https://www.huduser.gov/portal/datasets/usps_crosswalk.html), one of which we retrieved to process the Frontier and Remote Area codes.

* **Google Maps API Geocoder**: used to geocode hospitals; documentation available [here](https://developers.google.com/maps/documentation).

#### Dependencies

Required dependencies can be found in `requirements.txt`.

### Division of Labor

Ashlynn Wimer:
* Wrote the following scripts:
  * `CleanHospitals.py`: Script that performs a record linkage across our hospital datasets to create a hospital table.
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

Xuzhou Ding: