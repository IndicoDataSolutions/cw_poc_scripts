"""
Functions to generate comparisons between ground truth and predictions
"""

import os
import json
import pandas as pd

from collections import defaultdict

from utils import (
    files_from_directory,
    change_file_extension,
    read_json,
    pageFilename
)

model = 'tenancy_schedule'

prediction_suffix = ' Predicted'
confidence_suffix = ' Confidence'

columns = ['Unit', 'Tenant', 'Floor Area SqFt', 'Car Parking', 'Lease Term',
           'Lease Start', 'Lease Expiry', 'Rent Per Annum', 'Rent Per SqFt',
           'Next Review', 'Break Options', 'Comments', 'ERV Per Annum',
           'ERV Per SqFt', 'Inside 1954']

prediction_dir = '/home/fitz/Documents/POC/cw_poc_scripts/output/predictions/'
prediction_files_dir = os.path.join(prediction_dir, model)
dst_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/predictions/tenancy_schedule_extractions.xlsx'
# get answer key
# ToDo: make read_answer_key function
dfs = {}
prediction_files = files_from_directory(prediction_files_dir)

for prediction_file in prediction_files:

    filename = os.path.basename(prediction_file)
    column_order = []
    # create prediction and confidence columns
    for column in columns:
        prediction_column = column + prediction_suffix
        confidence_column = column + confidence_suffix
        column_order.extend([prediction_column, confidence_column])


    # add prediction and confidence values to comparison dataframe
    prediction_output = defaultdict(list)

    # open prediction file
    with open(prediction_file) as f:
        predictions = json.load(f)

    # get full predictions
    for prediction in predictions:
        label = prediction['label']
        prediction_label = label + prediction_suffix
        confidence_label = label + confidence_suffix

        text = prediction['text']
        confidence = prediction['confidence'][label]

        prediction_output[prediction_label].append(text)
        prediction_output[confidence_label].append(confidence)

    # make sure all columns are the same length to save to df
    lengths = {
        label_name: len(prediction_output[label_name])
        for label_name in prediction_output
        }

    if(lengths):
        max_length = max(lengths.values())
        for label_name in prediction_output:
            n_vals = max_length - lengths[label_name]
            prediction_output[label_name].extend([None]*n_vals)

        # create dataframe
        comparison_df = pd.DataFrame.from_dict(prediction_output)

        # handle case where certain labels are not calculated
        missing_col = [col for col in column_order if col not in comparison_df.columns]
        for col in missing_col:
            comparison_df[col] = None
        dfs[filename] = comparison_df[column_order]
    else:
        dfs[filename] = pd.DataFrame({})

# save files
with pd.ExcelWriter(dst_path) as writer:
    for filename, df in dfs.items():
        df.to_excel(writer, sheet_name=filename, index=False)
