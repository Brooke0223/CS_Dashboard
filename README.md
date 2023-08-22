# Michigan Controlled Substance Dashboard


## Description

The "Michigan Controlled Substance Dashboard" is a dynamic Power BI visualization that utilizes data science techniques to analyze and extract meaningful insights into Controlled Substance Prescribing Practices. This initiative leverages extensive and publicly accessible datasets to craft an immersive visualization tool, fostering an enhanced comprehension of controlled substance prescription trends within the state of Michigan.

## Project Objectives

The primary objectives of this project are as follows:

- **Educational Integration**: Offer a valuable learning opportunity for Computer Science students by integrating the project's analytical database into Oregon State University's CS-340 course, providing practical experience in data science techniques and database concepts.
- **User-Focused Tool**: Develop a dashboard that holds promising potential for use by healthcare providers, legislators, public health organizations, and anyone interested in understanding controlled substance prescribing trends.

## Features

- Interactive visualizations that enable users to explore controlled substance prescribing practices over time.
- Comparative analysis of different types of controlled substances and their prescription patterns.
- Geospatial visualizations showcasing prescription hotspots across different regions in Michigan.
- Trends analysis to identify potential shifts in prescribing practices and their implications.
- User-friendly interface that allows users to customize and filter data according to their specific interests.
- Integration potential with educational curricula for a hands-on learning experience.


## Datasets

The project utilizes publicly-accessible datasets. 
- Controlled Substance Data: Prescription data draws upon Michigan's Annual Drug Utilization Reports. Datasets are available for download [here](https://www.michigan.gov/lara/bureau-list/bpl/health/maps/reports).
- Population Estimates: Population estimates draw upon comprehensive data sourced from the National Center for Health Statistics (NCHS). Datasets are available for download [here](https://vitalstats.michigan.gov/osr/Population/npPopAgeGroupSlider.asp?AreaType=C).


## Data Handling
### Data Discovery
- Conducted preliminary exploratory analysis of CSV data using Pandas to understand distributions, ranges, and potential issues.

### Data Structuring
- Mapped age-bracket categories in the Population datasets to match Controlled Substance datasets, ensuring uniformity for cross-dataset analysis.
- Consolidated patients/providers by counties in datasets for years 2021-2022, disregarding zip codes to focus on counties; any data pertaining to patients/providers in different zip codes but the same county were aggregated to maintain consistency with previous years’ datasets.

### Data Cleaning
- Converted relevant data ('Total_Prescriptions', 'Total_Units', 'Total_Patients', 'Total_Days_Supply') to integer datatype.
- Handles special values by converting “N/A” to “NULL” for SQL insertion commands.
- Ensured consistency in categorical data across different reporting years (e.g. “3” vs. “Schedule 3”).
- Trimmed and formatted string data to ensure uniformity and avoid mismatch due to whitespace.

### Data Enriching
- Integrated Population dataset, enriching prescribing trends with broader demographic context.

### Data Validation
- Validated integer data fields (e.g. 'Total_Prescriptions', 'Total_Units', 'Total_Patients', 'Total_Days_Supply').
- Checked for missing values to ensure data completeness.
- Verified data integrity through mathematical computation accuracy assessment.
- Verified MME calculations present only for opiate drugs.
- Verified null and non-integer values in population data.

### Data Integrity Checks
- Examined data consistency against logical constraints and patterns.

### Outlier Detection and Handling
- Detected and managed outliers for robust analysis.

### Data Publishing
- Transformed divergent CSV data into structured DDL using Python and Pandas, forming a foundation for analysis.

### Documentation
- Created comprehensive documentation outlining transformations, assumptions, and methods for transparency.

### Quality Control
- Implemented quality control processes to validate adherence to best practices.


## Contribution Guidelines

Contributions to this project are welcome! If you find any issues or have suggestions for improvement, please create a pull request. For major changes, please open an issue first to discuss the proposed changes.