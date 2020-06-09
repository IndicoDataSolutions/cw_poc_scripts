import pandas as pd
import re
from price_parser import Price


def whitespace_cleaner(string):
    clean_key = ' '.join(string.split())
    return clean_key


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


def post_process_percentage(df, column):
    df[column] = df[column].str.replace(r'[a-zA-z\s%,\-\+\(\)\*\/]+', '')
    df[column] = df[column].str.replace(r'[\.]$', '')
    df[column] = df[column].str.replace(r'^[\.]', '')
    mask = df[column] != ''
    df.loc[mask, column] = df.loc[mask, column].astype(float)
    return df[column]


def post_process_address(df, column):
    df[column] = df[column].str.replace(r'[^\w\s]', ' ')
    df[column] = df[column].str.replace(r'\s+', ' ')
    return df[column]

comparison_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/investment_summary_extraction.csv'
post_processed_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/investment_summary_extraction_final.csv'
comparison_df = pd.read_csv(comparison_path)
comparison_df.fillna('', inplace=True)


fields = ['Area', 'Build Date', 'Purchase Price', 'NIY', 'WAULT Expiry', 'WAULT Breaks', 'Address', 'Postal Code']
fields = [field + ' Predicted' for field in fields]
for field in fields:
    comparison_df[field] = comparison_df[field].astype(str)
    

comparison_df['Address Predicted'] = post_process_address(comparison_df, 'Address Predicted')
comparison_df['Address Predicted'] = comparison_df['Address Predicted'].apply(whitespace_cleaner)
comparison_df['Purchase Price'] = comparison_df['Purchase Price'].apply(price_cleaner)
comparison_df['Postal Code'] = comparison_df['Postal Code'].str.replace(r'\W+', '')
comparison_df['Area Predicted'] = comparison_df['Area Predicted'].str.replace(r'\D+', '')
comparison_df['NIY Predicted'] = post_process_percentage(comparison_df, 'NIY Predicted')
comparison_df['WAULT Expiry Predicted'] = post_process_percentage(comparison_df, 'WAULT Expiry Predicted')
comparison_df['WAULT Breaks Predicted'] = post_process_percentage(comparison_df, 'WAULT Breaks Predicted')


comparison_df.set_index('Filename', inplace=True)
comparison_df.to_csv(post_processed_path)