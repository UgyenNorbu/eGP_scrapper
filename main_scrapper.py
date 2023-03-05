"""Scrap e-GP website"""

# Import packages

import time
from datetime import date
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Initialize webdriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Connect to the url
time.sleep(1)
URL = 'https://www.egp.gov.bt/resources/common/TenderListing.jsp?h=t'
driver.get(URL)

# Identify HTML element for the table with ID = 'resultTable' and create a pandas dataframe
table = driver.find_element(By.CSS_SELECTOR, "table#resultTable").get_attribute("outerHTML")
my_df = pd.read_html(table)[0]

time.sleep(3)
driver.quit()

# Clean the dataframe

# Drop the 1st column 'Sl. no.'
my_df.drop('Sl. No.', axis = 1, inplace = True)

# Generate col_names

def get_col_names(input_df):
    """This function will list all the dataframe column titles"""
    df_old_colnames = []
    for i in range(input_df.shape[1]):
        _ = input_df.columns[i]
        df_old_colnames.append(_)
    return df_old_colnames

# Define helper function to split and strip col_names

def split_drop_cols(col_name, input_df, delim):
    """This function splits dataframe columns at delim and drop the original column"""
    if len(col_name.split(delim)) == 1:
        new_col_names = col_name
        input_df[new_col_names] = input_df[col_name]
    else:
        new_col_names = col_name.split(delim)
        new_col_names = [x.strip() for x in new_col_names]
        split_len = len(new_col_names) - 1
        input_df[new_col_names] = input_df[col_name].str.split(delim, n = split_len, expand = True)
        input_df.drop(columns = col_name, axis = 1, inplace = True)
    return input_df

# Input col_names and df to helper function
N = len(get_col_names(my_df))
input_colname = get_col_names(my_df)

for i in range(N):
    if i < (N - 1):
        split_drop_cols(input_colname[i], my_df, ',')
    else:
        split_drop_cols(input_colname[i], my_df, '|')

# Export the data
DATE = str(date.today())
FILE_NAME = DATE + '_data.csv'

my_df.to_csv(FILE_NAME)