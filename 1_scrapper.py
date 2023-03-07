''' INITIALIZE THE WEB LINK '''
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




''' SCRAP THE HTML TABLE '''

# Identify HTML element for the table with ID = 'resultTable' and create a pandas dataframe
def read_table_to_df():
    table = driver.find_element(By.CSS_SELECTOR, "table#resultTable").get_attribute("outerHTML")
    table_df = pd.read_html(table)[0]
    return table_df

# Find how many number of pages long a HTML table is

def find_table_len():
    pg_no = driver.find_element(By.ID, 'pageTot').text
    return int(pg_no)

# Read paginated table here
def scrap_table_seq(pg_no = find_table_len()):
    master_col_names = ['Sl. No.',
                         'Tender ID,  Reference No,  Public Status',
                         'Procurement Category,  Title',
                         'Hierarchy Node',
                         'Type,  Method',
                         'Publishing Date & Time | Closing Date & Time']
    master_df = pd.DataFrame(columns= master_col_names)
    print(master_df)
    if pg_no == 1:
        my_df = read_table_to_df()
        master_df = pd.concat([master_df, my_df])
    else:
        for i in range(1, pg_no + 1):
            pg_no_form = driver.find_element(By.ID, 'dispPage')
            pg_no_form.clear()
            pg_no_form.send_keys(i)
            go_to_page = driver.find_element(By.ID, 'btnGoto')
            go_to_page.click()
            my_df = read_table_to_df()
            time.sleep(1)
            master_df = pd.concat([master_df, my_df], ignore_index=True)
    return master_df

time.sleep(1)
compiled_df = scrap_table_seq()
driver.quit()


''' CLEAN AND EXPORT THE DATA '''

# Clean the dataframe

# Drop the 1st column 'Sl. no.'
compiled_df.drop('Sl. No.', axis = 1, inplace = True)

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
input_colname = get_col_names(compiled_df)
N = len(input_colname)

for i in range(N):
    if i < (N - 1):
        split_drop_cols(input_colname[i], compiled_df, ',')
    else:
        split_drop_cols(input_colname[i], compiled_df, '|')

# Export the data
DATE = str(date.today())
FILE_NAME = DATE + '_data.csv'

compiled_df.to_csv(FILE_NAME)