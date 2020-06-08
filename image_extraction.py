import fitz
import os
import click
import click_pathlib
from tqdm import tqdm

from utils import files_from_directory


def extract_images_from_file(pdf_filepath, dst_folder):
    """
    Use PyMuPDF to extract all images from a PDF file and save to dst_folder

    Code derived from: https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python/47877930#47877930
    Arguments:
        filepath {str} -- path to Brochure pdf file
        dst_folder {str} -- path to folder to save png output

    """
    filename = os.path.basename(pdf_filepath)
    filename_no_ext = os.path.splitext(filename)[0]
    doc = fitz.open(pdf_filepath)

    for i in range(len(doc)):
        for img_num, img in enumerate(doc.getPageImageList(i)):
            xref = img[0]
            save_name = "%s-p%s-%s.png" % (filename_no_ext, i, xref)
            save_path = os.path.join(dst_folder, save_name)
            try:
                pix = fitz.Pixmap(doc, xref)
                if pix.colorspace.name != 'DeviceCMYK':   # this is GRAY or RGB
                    pix.writePNG(save_path)
                else:               # CMYK: convert to RGB first
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                    pix.writePNG(save_path)
                    pix = None
                pix = None
            except Exception as e:
                print(e)
                print("continuing image extraction")
                continue


def image_extraction_driver(src_dir: str, dst_folder: str):
    """
    Script to run pdf extraction on src_folder and save extraction
    output to dst_folder.
    """
    pdf_paths = files_from_directory(src_dir)
    for pdf_path in tqdm(pdf_paths):
        extract_images_from_file(pdf_path, dst_folder)
    print("Generated image extractions")


@click.command()
@click.argument('src_dir', type=click_pathlib.Path(exists=True))
@click.argument('dst_folder')
def main(src_dir: str, dst_folder: str):
    """
    Script to run pdf extraction on src_folder and save extraction
    output to dst_folder.
    """
    image_extraction_driver(src_dir, dst_folder)


if __name__ == '__main__':
    main()
