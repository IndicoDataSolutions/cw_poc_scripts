import pandas as pd
from price_parser import Price
import re 


def price_cleaner(string):
    match = re.match("[0-9]+\s[0-9][0-9]", string)
    if match:
        clean_string = string.replace(' ', '.')
    else:
        price = Price.fromstring(string)
        if price.amount:
            clean_string = str(round(price.amount, 2))
        else:
            clean_string = ''
    return clean_string


def post_process_address(df, column):
    df[column] = df[column].str.replace(r'[^\w\s]', ' ')
    df[column] = df[column].str.replace(r'\s+', ' ')
    df[column] = df[column].str.strip()
    return df[column]


def drop_the(df, column):
    df[column] = df[column].str.upper()
    df[column] = df[column].str.replace('THE', '')
    df[column] = df[column].str.strip()
    return df[column]

def post_process_percentage(df, column):
    df[column] = df[column].str.replace(r'[a-zA-z\s%,\-\+\(\)\*]+', '')
    df[column] = df[column].str.replace(r'[\.]$', '')
    df[column] = df[column].str.replace(r'^[\.]', '')
    mask = df[column] != ''
    df.loc[mask, column] = df.loc[mask, column].astype(float)
    return df[column]


comparison_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/unstructured_tenancy_extraction.csv'
post_processed_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/unstructured_tenancy_extraction_final.csv'

comparison_df = pd.read_csv(comparison_path)
comparison_df.fillna('', inplace=True)

comparison_df['Floor Area Predicted'] = comparison_df['Floor Area Predicted'].astype(str)

filenames = comparison_df['Filename']


comparison_df['Tenant Predicted'] = post_process_address(comparison_df, 'Tenant Predicted')
comparison_df['Lease Start Predicted'] = post_process_address(comparison_df, 'Lease Start Predicted')
comparison_df['Lease Expiry Predicted'] = post_process_address(comparison_df, 'Lease Expiry Predicted')
comparison_df['Next Review Predicted'] = post_process_address(comparison_df, 'Next Review Predicted')
comparison_df['Break Option Predicted'] = drop_the(comparison_df, 'Break Option Predicted')
comparison_df['Rent Per Annum Predicted'] = comparison_df['Rent Per Annum Predicted'].apply(price_cleaner)
comparison_df['Rent Per SqFt Predicted'] = comparison_df['Rent Per SqFt Predicted'].apply(price_cleaner)
comparison_df['Floor Area Predicted'] = comparison_df['Floor Area Predicted'].apply(price_cleaner)

comparison_df['Filename'] = filenames
comparison_df.set_index('Filename')
comparison_df.to_csv(post_processed_path)
