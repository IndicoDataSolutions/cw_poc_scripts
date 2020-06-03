import fitz
import os
import click
import click_pathlib


def extract_images_from_file(pdf_filepath, dst_folder):
    """
    Use PyMuPDF to extract all images from a PDF file and save to dst_folder

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
                if pix.colorspace.name != 'DeviceCMYK':       # this is GRAY or RGB
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


@click.command()
@click.argument('filepath', type=click_pathlib.Path(exists=True))
@click.argument('dst_folder')
def main(filepath: str, dst_folder: str):
    """
    Script to run pdf extraction on src_folder and save extraction
    output to dst_folder.
    """
    extract_images_from_file(filepath, dst_folder)
    print("Generated image extractions")


if __name__ == '__main__':
    main()
