"""
This script demonstrates a sample workflow to get predictions from a single
Brochure PDF. The end result is a set of CSV files containing predictions.

The following models are used to predict on documents:

Text
----
Page Classification
Address Extraction
Investment Summary Extraction
Tenancy Schedule Extraction
Unstructured Tenancy Extraction

Images
------
Building Classification
Secondary Building Classification

To run:
python3 workflow.py <path to pdf_file> <output_folder>

"""

# Text Model IDs
PAGE_CLASSIFIER_MODEL_ID = 29828
ADDRES_EXTRACTION_MODEL_ID = 29352
INVESTMENT_EXTRACTION_MODEL_ID = 28428
TENANCY_SCHEDULE_EXTRACTION_MODEL_ID = 30006
UNSTRUCTURED_TENANCY_EXTRACTION_MODEL_ID = 29843

# Image Classifiers
BUILDING_CLASSIFIER = 29348
SECONDARY_BUILDING_CLASSIFIER = 30112
