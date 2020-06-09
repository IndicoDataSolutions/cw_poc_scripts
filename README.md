## Script to demonstrate indico API w/ linked Models

Sample code to demonstrate Indico API and linked models for 
Cushman & Wakefield Document Classification & Extraction. There are many ways to filter/output 
the results and this script demonstrates a sample pipeline for a single PDF document. 
 

This script is designed to take a file path to a PDF document and perform the following steps: 
          #### Document Workflow                                 #### Image Workflow
    
(1) Perform page-by-page OCR on the document                 Extract images from document
(2) Send the raw text to the page classifier model           Send images to building image classifier
(3) Send classified pages to relevant annotation model       Send buidling images to secondary building classifier
(4) Write the results to a CSV                               Write results to a CSV
 


### Requirements

Tested with Python 3.8.2, but should work Python 3.6+

To run the script, place your api_token file into this directory (which can be downloaded from 
app.indico.io on your account page)


### Script Descriptions

The scripts in this repository are meant to simulate the process of the POC
particularly the blind test.  Since each step of the process can take an
extended period of time, each step has been broken out into a script which
saves intermediate output.  Please follow the order of scripts below for
successful test runs.

#### Text models
1) pdf_extraction.py - Extract plaintext data from source pdf files
2) page_classification.py - Run predictions on each page plaintext to classify pages
                            of source pdfs
3) extraction_predictions.py - Run each classified page through it's associated extraction model
4) extraction_csv.py - create csv of predictions for Address, Investment Summary and Unstructured Tenancy analysis
5) table_csv.py - create excel file of predictions for Tenancy Table
6) post_process_(model).py - run normalization steps on extraction predictions


#### Image models
1) image_extraction.py - extract all images from source pdfs
2) upload_images.py - upload image data to indico storage
3) image_classification.py - run building classifier models to get predictions