# Michigan Controlled Substance Dashboard


## Description

The "Michigan Controlled Substance Dashboard" has been developed as a dynamic Power BI visualization, utilizing data science techniques to analyze and derive meaningful insights into Controlled Substance Prescribing Practices from 2013-2022. This initiative capitalizes on extensive and publicly accessible datasets, crafting an immersive visualization tool that fosters an enriched understanding of controlled substance prescription trends within the state of Michigan.

## Project Objectives

The primary objectives of this project are as follows:

- **User-Focused Tool**: The dashboard of this project holds the promise of being utilized by healthcare providers, legislators, public health organizations, and those interested in comprehending trends in controlled substance prescribing.

- **Educational Integration**: The analytical database that underpins the project will be integrated into Oregon State University's CS-340 course, delivering practical experience in data science techniques and database concepts to students enrolled in OSU's Bachelor of Computer Science program.

## Features

- Interactive displays to explore controlled substance prescribing practices over time.
- Comparative analysis of different controlled substances categories and patient age-brackets.
- Geospatial representations showcasing prescription hotspots across Michigan counties.
- Trends analysis to identify potential shifts in prescribing practices and their implications.
- A dynamic interface that supports custom data filters.


## Datasets

The project utilizes publicly-accessible datasets. 
- Controlled Substance Data: Prescription data draws upon Michigan's Annual Drug Utilization Reports. Datasets are available for download [here](https://www.michigan.gov/lara/bureau-list/bpl/health/maps/reports).
- Population Estimates: Population estimates draw upon comprehensive data sourced from the National Center for Health Statistics (NCHS). Datasets are available for download [here](https://vitalstats.michigan.gov/osr/Population/npPopAgeGroupSlider.asp?AreaType=C).


## Data Handling
Data Discovery
- A preliminary exploratory analysis of CSV data was performed using Pandas to discern distributions, ranges, and potential issues.

Data Structuring
- Aligned age-bracket categories within the Population datasets to correspond with those in the Controlled Substance datasets, ensuring uniformity for cross-dataset analysis.
- Consolidated data for patients/providers with the same county but different zip codes (reporting years 2021-2022) to ensure consistency with earlier datasets and maintain county as the primary unit of consideration.

Data Cleaning
- Converted pertinent data ('Total_Prescriptions', 'Total_Units', 'Total_Patients', 'Total_Days_Supply') to integer datatype.
- Managed special values by converting “N/A” to “NULL” for SQL insertion commands.
- Maintained categorical data consistency across diverse reporting years (e.g. “3” vs. “Schedule 3”).
- Trimmed and formatted string data to ensure uniformity and prevent whitespace mismatches.

Data Enriching
- Integrated the Population dataset to provide a broader demographic context for prescribing trends.

Data Validation
- Validated integer data fields (e.g. 'Total_Prescriptions', 'Total_Units', 'Total_Patients', 'Total_Days_Supply').
- Scrutinized for missing values to ensure data completeness.
- Verified data integrity through accuracy assessment of mathematical computations.
- Verified MME calculations were present only for opiate drugs.

Data Integrity Checks
- Examined data consistency against logical constraints and patterns.

Outlier Detection and Handling
- Detected and managed outliers for robust analysis.

Data Publishing
- Transformed divergent CSV data into structured DDL using Python and Pandas, forming a foundation for subsequent analysis.

Documentation
- Created comprehensive documentation outlining transformations, assumptions, and methods for transparency.

Quality Control
- Implemented quality control processes to validate adherence to best practices.


## Contribution Guidelines

Contributions to this project are welcome! If you find any issues or have suggestions for improvement, please create a pull request. For major changes, please open an issue first to discuss the proposed changes.