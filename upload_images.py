"""
Script to upload images to indico
"""
import os
from tqdm import tqdm
import json
import pandas as pd
import click
import click_pathlib

from config import PROD_CLIENT
from indico.queries import UploadDocument
from utils import files_from_directory


def upload_to_indico_storage(filepath):
    """
    Upload document from filepath to indico storage and return the storage
    path
    """
    image = PROD_CLIENT.call(
            UploadDocument(files=[filepath])
        )
    path = json.loads(image[0]["filemeta"])["path"]
    path = "indico-file:///storage" + path
    return path


def image_upload_driver(src_dir):
    """
    Iterate through all png files in src_dir and upload to indico. Save
    mapping of original filepath -> storage location to image_storage_map.csv
    in the src_dir
    """

    filepaths = files_from_directory(src_dir, regex='*.png')
    uploads = {
        'Filename': [],
        'Storage Location': []
        }

    for filepath in tqdm(filepaths):
        storage_path = upload_to_indico_storage(filepath)
        uploads['Filename'] = os.path.basename(filepath)
        uploads['Storage Location'] = storage_path

    # save file to storage path mapping
    output_filename = 'image_storage_map.csv'
    output_path = os.path.join(src_dir, output_filename)
    df = pd.DataFrame(uploads)
    df.to_csv(output_path, index=False)


@click.command()
@click.argument('src_dir', type=click_pathlib.Path(exists=True))
def main(src_dir):
    image_upload_driver(src_dir)


if __name__ == '__main__':
    main()
