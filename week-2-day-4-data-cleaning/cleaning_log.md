# Data Cleaning Log

## Dataset
Sample employee dataset used for Week 2 Day 4 practice.

## Missing values before cleaning
name          1
age           1
salary        1
city          1
department    0

## Cleaning decisions
- Trimmed whitespace from text columns.
- Standardized names and cities using title case.
- Standardized department values to uppercase.
- Imputed missing age using the mean.
- Imputed missing salary using the median.
- Imputed missing city using the mode.
- Replaced missing names with 'Unknown'.
- Demonstrated forward-fill on a separate department Series.
- Corrected ages outside the 0-100 range using the median.
- Detected numeric outliers using the 1.5 x IQR rule.
- Capped detected numeric outliers at the IQR boundaries.
- Removed duplicate rows where present.

## Imputation reference values
- Original age mean: 64.60
- Original age median: 30.00
- Original salary median: 45000.00
- City mode: Bangalore
- Missing departments after forward-fill: 0

## Invalid ages
- Invalid ages corrected: 1

## Outlier detection
- age: 1 outliers detected; capped to [15.00, 51.00]
- salary: 1 outliers detected; capped to [20625.00, 65625.00]

## Before-and-after quality comparison
        Metric  Before  After
          Rows       6      6
Missing values       4      0
Duplicate rows       0      0

## Final missing values
name          0
age           0
salary        0
city          0
department    0