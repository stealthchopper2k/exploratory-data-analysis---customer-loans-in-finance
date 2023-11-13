# Exploratory Data Analysis - Customer Loans in Finance

# Purpose

This project aims to perform EDA on loan portfolio and use statistical and data visualisation techniques to uncover patterns, relationships, and anomalies in loan data. We also prepare the data for ML algorithms by fixing impact of outliers and data skewness. Furthermore visualise the future payments and attempt to correlate parameters of user data to failing loan payments

This is with the purpose of enabling the business to make more informed decisions about loan approvals, pricing, and risk management.

# Installation Instructions
1. ```pip install -r requirements.txt```


# Running Instructions
1. Run the main.ipynb file

# File Modules
1. *./format.py* Class to convert columns into correct format such as categorical columns, more efficient data types and numerical columns that are better fit into numericals, as well as dates.
2. *./info.py* Provides information about the shape of the data, skewness numericals, missing data and general statistics where needed.
3. *./plotter.py* Provides visualisation methods for the data such as histograms, KDE, qq_plot and ability to do so across multiple columns.
4. *./transform.py* Responsible for imputation and transformation of data to prepare for more ML applications via creating a normal distribution.

# Note
I use __main__ within each of these modules to play around with the data initially and then finally use main.ipynb to follow a specific structure