import pandas as pd
from os import listdir

def get_file_name(n, file_path = 'scrapped_csv/', ext = '.csv'):
    """ Helper function to get filename """
    dir_content = listdir(file_path)
    file_list = []
    for i in dir_content:
        if i.endswith(ext):
            file_list.append(i)
    file_list.sort()
    return file_list[-n]

# Get names of current and previous data
CURRENT_FILE_NAME = get_file_name(1)
PREV_FILE_NAME = get_file_name(2)

# Read current and previous data as dataframe
current_df = pd.read_csv('scrapped_csv/' + CURRENT_FILE_NAME, index_col=[0])
prev_df = pd.read_csv('scrapped_csv/' + PREV_FILE_NAME, index_col=[0])

def anti_join_dfs(df_1 = prev_df, df_2 = current_df):
    ''' Helper function to perform anti-join of two dfs '''
    df_1 = df_1.apply(lambda x: x.str.strip())
    df_2 = df_2.apply(lambda x: x.str.strip())
    filt = df_2['Tender ID'].isin(df_1['Tender ID'])
    output = df_2[filt]
    return output

def cleaned_current_data():
    ''' Helper function to clean '''
    df = anti_join_dfs()
    df.dropna(how = 'any', inplace=True)
    goods_df = df.loc[(df['Procurement Category'].str.contains('Goods')) & (df['Public Status'] == 'Live')]
    goods_df.reset_index(drop = True, inplace = True)
    return goods_df

def export_to_excel(df = cleaned_current_data(), filename = CURRENT_FILE_NAME):
    ''' Export clean data as excel '''
    filename = 'export_xl/' + CURRENT_FILE_NAME.split('.')[0] + '.xlsx'
    df.to_excel(filename, index=False)

def main_DA():
    ''' Main wrapper function for the exploratory data analysis '''
    cleaned_current_data()
    export_to_excel()