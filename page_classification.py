"""
functions to handle page classification
"""

import pandas as pd
import os
import click
import click_pathlib

from utils import (
    files_from_directory,
    change_file_extension,
    read_json,
)
from predictions import predict, get_top_classification


PAGE_CLASSIFIER_MODEL_ID = 29828


def page_classification_driver(
    pdf_extractions_path,
    dst_folder,
    output_filename='page_classifications_output.csv'
):
    """
    Driver to compute page classifcations for all pdf pages in the pdf
    documents in pdf_extractions_path, save to dst_folde/output_filename
    """

    # get all pdf_extraction_files
    extraction_paths = files_from_directory(pdf_extractions_path)
    page_dict = {
        'Filename': [],
        'Page Number': [],
        'Prediction': [],
        'Confidence': []
    }

    samples = []
    for extraction_path in extraction_paths:
        filename = change_file_extension(extraction_path, '.pdf')
        page_extractions = read_json(extraction_path)
        for page in page_extractions:

            text = page['pages'][0]['text']
            samples.append(text)
        n_pages = len(page_extractions)
        page_dict['Filename'].extend([filename]*n_pages)
        page_dict['Page Number'].extend(range(1, n_pages+1))

    prediction_dicts = predict(samples, PAGE_CLASSIFIER_MODEL_ID)
    predictions, confidences = get_top_classification(prediction_dicts)
    page_dict['Prediction'] = predictions
    page_dict['Confidence'] = confidences

    # Save out predictions to csv file
    df = pd.DataFrame(page_dict)
    output_path = os.path.join(dst_folder, output_filename)
    df.to_csv(output_path, index=False)


@click.command()
@click.argument('src_dir', type=click_pathlib.Path(exists=True))
@click.argument('dst_folder')
@click.option('--output-filename', default='page_classifications_output.csv')
def main(src_dir: str, dst_folder: str, output_filename: str):
    """
    Script to run pdf extraction on src_folder and save extraction
    output to dst_folder.
    """
    page_classification_driver(src_dir, dst_folder, output_filename)


if __name__ == '__main__':
    """
    pdf_extractions_path = '/home/fitz/Documents/POC/cw_poc_scripts/output/doc_extractions/text'
    dst_folder = '/home/fitz/Documents/POC/cw_poc_scripts/output/predictions'
    page_classification_driver(pdf_extractions_path, dst_folder)
    """
    main()
