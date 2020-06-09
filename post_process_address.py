import pandas as pd
import numpy as np
import os


# post process Address

comparison_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/address_extraction.csv'
post_processed_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output/address_extraction_final.csv'
comparison_df = pd.read_csv(comparison_path)
comparison_df.fillna('', inplace=True)

address_columns = ['Address Predicted']

# Remove unnesccessary punctuation from address
for address_column in address_columns:
    comparison_df[address_column] = comparison_df[address_column].str.replace(r'[^\w\s]', ' ')
    comparison_df[address_column] = comparison_df[address_column].str.replace(r'\s+', ' ')

# remove all white space and punctuation from postal code
comparison_df['Postal Code Predicted'] = comparison_df['Postal Code Predicted'].str.replace(r'\W+', '')

string_cols = ['Address Predicted',  'Postal Code Predicted' ]
comparison_df[string_cols] = comparison_df[string_cols].apply(lambda x: x.str.upper())


comparison_df.set_index('Filename', inplace=True)
comparison_df.to_csv(post_processed_path)



