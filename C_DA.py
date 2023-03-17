import pandas as pd
from datetime import date
from os import listdir

def get_file_name(file_path = 'scrapped_csv/', ext = '.csv'):
    """ Helper function to get filename """
    dir_content = listdir(file_path)
    file_list = []
    for i in dir_content:
        if i.endswith(ext):
            file_list.append(i)
    file_list.sort()
    return file_list

def anti_join_dfs():
    ''' Helper function to perform anti-join of two dfs '''
    CURRENT_FILE_NAME = get_file_name()[-1]
    PREV_FILE_NAME = get_file_name()[-2]

    current_df = pd.read_csv('scrapped_csv/' + CURRENT_FILE_NAME, index_col=[0])
    prev_df = pd.read_csv('scrapped_csv/' + PREV_FILE_NAME, index_col=[0])

    prev_df = prev_df.apply(lambda x: x.str.strip())
    current_df = current_df.apply(lambda x: x.str.strip())
    filt = current_df['Tender ID'].isin(prev_df['Tender ID'])
    output = current_df[filt]
    return output

def cleaned_current_data():
    ''' Helper function to clean '''
    my_files = get_file_name()
    if len(my_files) == 1:
        df = pd.read_csv('scrapped_csv/' + my_files[0], index_col=[0])
        df = df.apply(lambda x: x.str.strip())
    else:
        df = anti_join_dfs()
    df.dropna(how = 'any', inplace=True)
    filt = (df['Procurement Category'].str.contains('Goods')) & (df['Public Status'] == 'Live')
    goods_df = df.loc[filt]
    goods_df.reset_index(drop = True, inplace = True)
    return goods_df

def name_export_xl():
    ''' Create name for data to export as excel '''
    DATE = str(date.today())
    name = 'export_xl/' + DATE + '.xlsx'
    return name

def main_DA():
    ''' Main wrapper function for the exploratory data analysis '''
    cleaned_current_data()
    df = cleaned_current_data()
    export_filename = name_export_xl()
    df.to_excel(export_filename, index=False)