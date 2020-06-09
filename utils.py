import os
import json
import glob
from PyPDF2 import PdfFileReader, PdfFileWriter
from typing import Iterable


def pageFilename(filepath, page):
    """
    Append page to filename, assumes filename has an extension
    """

    filename, extension = os.path.splitext(filepath)
    page_filepath = f"{filename}_page_{page}{extension}"
    return page_filepath


def read_json(filename):
    with open(filename) as f:
        json_obj = json.load(f)
    return json_obj


def files_from_directory(src_dir, regex='*.*'):
    """
    return a list of all files in src_dir that match the regex
    """
    filename_regex = os.path.join(src_dir, regex)
    filelist = glob.glob(filename_regex)
    return filelist


def change_file_extension(filename, extension):
    filename_no_ext = os.path.splitext(filename)[0]
    new_filename = filename_no_ext + extension
    return new_filename


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


def separate_pdf(
    pdf_input_path: str,
    pdf_output_path: str,
    pages: Iterable
) -> None:
    """
    Extract all specified pages and save to pdf_output_path
    """

    with open(pdf_input_path, 'rb') as f:
        pdf = PdfFileReader(f)
        if pdf.isEncrypted:
            pdf.decrypt('')

        for page in pages:
            # convert page to 0 index val
            page -=1
            out_pdf = PdfFileWriter()
            output_filepath = pageFilename(pdf_output_path, page)
            out_pdf.addPage(pdf.getPage(page))
            with open(output_filepath, 'wb') as f:
                out_pdf.write(f)
