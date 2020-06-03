"""
Generate pdf extractions
"""
import os
import json
import click
import click_pathlib

from config import PROD_CLIENT, detailed_pdf_extraction_config

from indico.queries.documents import DocumentExtraction
from indico.queries import JobStatus, RetrieveStorageObject


def save_extraction(extraction, src_doc, dst_folder):
    """
    Save json extraction to dst_folder with the name of the src_doc file

    Arguments:
        config {dict} -- pdf extraction dictionary
        src_doc {str} -- path to Brochure pdf file
        dst_folder {str} -- path to save json output

    Returns:
        str -- output file path

    """
    filename = os.path.basename(src_doc)
    filename_no_ext = os.path.splitext(filename)[0]
    output_filename = filename_no_ext + '.json'
    output_filepath = os.path.join(dst_folder, output_filename)

    with open(output_filepath, 'w') as f:
        json.dump(extraction, f)

    return output_filepath


def pdf_extraction_call(pdf_filepath, client, config):
    """
    Given a filepath, run Indico document extraction and save json output to
    dst_folder

    Arguments:
        pdf_filepath {str} -- path to Brochure pdf file
        client {IndicoClient} -- IndicoClient object containing auth details
        config {dict} -- Indico Document extraction options

    Returns:
        dict -- pdf extraction of pdf_filepath

    """

    jobs = client.call(
        DocumentExtraction(
            files=[pdf_filepath],
            json_config=json.dumps(config)
        )
    )

    for i, j in enumerate(jobs):
        try:
            job = client.call(JobStatus(id=j.id, wait=True))
            doc_extract = client.call(RetrieveStorageObject(job.result))
        except Exception as e:
            print(e)
    return doc_extract


def pdf_extraction_driver(src_doc, dst_folder):
    """
    Given a filepath, run Indico document extraction and save json output to
    dst_folder witht the same name as the src_doc

    Arguments:
        filepath {str} -- path to Brochure pdf file
        dst_folder {str} -- path to folder to save json output

    Returns:
        str -- output file path

    """
    pdf_extraction = pdf_extraction_call(src_doc, PROD_CLIENT,
                                         detailed_pdf_extraction_config)
    output_filepath = save_extraction(pdf_extraction, src_doc, dst_folder)
    return output_filepath


@click.command()
@click.argument('filepath', type=click_pathlib.Path(exists=True))
@click.argument('dst_folder')
def main(filepath: str, dst_folder: str):
    """
    Script to run pdf extraction on src_folder and save extraction
    output to dst_folder.
    """
    output_filepath = pdf_extraction_driver(filepath, dst_folder)
    print(f"Generated pdf extraction at {output_filepath}")


if __name__ == '__main__':
    main()
