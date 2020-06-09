"""
Script to split pdf files into single page pdf files for upload to indico
teach.  The script will separate pdf pages and place into separate directory
according to predicted class
"""

import pandas as pd
import os
from collections import defaultdict
from utils import separate_pdf

data_dir = '/home/fitz/Documents/POC/cw_poc_scripts/output/predictions'
pdf_dir = '/home/fitz/Documents/POC/cw_poc_scripts/input_data'
output_path = os.path.join(data_dir, 'extraction_datasets')

page_classification_csv_filepath = os.path.join(data_dir, 'page_classifications_output.csv')
page_class_df = pd.read_csv(page_classification_csv_filepath)


folder_model_map = {
    'UNSTRUCTURED TENANCY': 'unstructured_tenancy',
    'TENANCY SCHEDULE': 'tenancy_schedule',
    'ADDRESS': 'address',
    'INVESTMENT': 'investment'
}

failed_files = defaultdict(list)
for model, folder in folder_model_map.items():
    extraction_dataset_path = os.path.join(output_path, folder)
    if not os.path.exists(extraction_dataset_path):
        os.mkdir(extraction_dataset_path)

    # filter page_classification by model type
    model_mask = page_class_df['Prediction'] == model
    model_test_df = page_class_df[model_mask]
    filepaths = pd.unique(model_test_df['Filename'])
    model_test_df.set_index('Filename', inplace=True)

    # iterate through file paths to split pdf
    for filepath in filepaths:
        filename = os.path.basename(filepath)
        pdf_filepath = os.path.join(pdf_dir, filename)
        output_filepath = os.path.join(extraction_dataset_path, filename)
        file_df = model_test_df.loc[[filepath]]
        page_numbers = file_df['Page Number'].to_list()

        # extract pdf page
        try:
            separate_pdf(pdf_filepath, output_filepath, page_numbers)
        except:
            failed_files[model].append(pdf_filepath)
            continue

print(failed_files)
