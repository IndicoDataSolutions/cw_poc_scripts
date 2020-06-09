"""
Functions to generate csv output for extraction models:
Address
Investment Summary
Unstructured Tenancy

Filename | 
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


models = ['address', 'investment_summary', 'unstructured_tenancy']
address_cols = ['Address', 'Postal Code']
investment_cols = ['Area', 'Build Date', 'Purchase Price', 'NIY',
                   'WAULT Expiry', 'WAULT Breaks', 'Address', 'Postal Code']

unstructured_tenancy_cols = ['Tenant', 'Lease Term', 'Lease Start',
                             'Break Option', 'Rent Per Annum', 'Rent Per SqFt',
                             'Lease Expiry', 'Next Review', 'Floor Area']
label_cols = [address_cols, investment_cols, unstructured_tenancy_cols]
prediction_suffix = ' Predicted'
confidence_suffix = ' Confidence'


src_dir = '/home/fitz/Documents/POC/cw_poc_scripts/output/predictions'
dst_dir = '/home/fitz/Documents/POC/cw_poc_scripts/output/final_output'

for model, label_cols in zip(models, label_cols):
    prediction_files_dir = os.path.join(src_dir, model)
    prediction_files = files_from_directory(prediction_files_dir)

    predictions_dict = defaultdict(dict)
    column_order = []
    # add columns to hold predictions and confidences
    for column in label_cols:
        prediction_column = column + prediction_suffix
        confidence_column = column + confidence_suffix
        column_order.extend([prediction_column, confidence_column])

    # add prediction and confidence values to comparison dataframe
    for prediction_file in prediction_files:
        predictions = read_json(prediction_file)
        filename = os.path.basename(prediction_file)

        # get full predictions
        full_prediction_output = defaultdict(lambda: defaultdict(list))
        for prediction in predictions:
            label = prediction['label']
            prediction_label = label + prediction_suffix
            confidence_label = label + confidence_suffix

            text = prediction['text']
            confidence = prediction['confidence'][label]

            full_prediction_output[label][prediction_label].append(text)
            full_prediction_output[label][confidence_label].append(confidence)

        # get only top predictions
        for label in full_prediction_output:
            prediction_label = label + prediction_suffix
            confidence_label = label + confidence_suffix
            predictions = full_prediction_output[label][prediction_label]
            confidences = full_prediction_output[label][confidence_label]

            highest_conf_ind = confidences.index(max(confidences))
            predictions_dict[filename][prediction_label] = (
                predictions[highest_conf_ind]
            )
            predictions_dict[filename][confidence_label] = (
                confidences[highest_conf_ind]
            )

    # save to CSV
    # Filename | Class(i) Prediction | Class(i) Confidence ...
    df = pd.DataFrame.from_dict(predictions_dict, orient='index')
    df.index.name = 'Filename'
    output_filename = f"{model}_extraction.csv"
    output_path = os.path.join(dst_dir, output_filename)
    df[column_order].to_csv(output_path)
