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
