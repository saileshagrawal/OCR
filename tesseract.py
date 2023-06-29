import cv2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import numpy as np
#from docx import Document


# Set the tesseract path to the location of your tesseract executable
#pytesseract.pytesseract.tesseract_cmd = r'"C:\Program Files\Tesseract-OCR\tesseract.exe"'

# def preprocess(image):
#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Noise removal with iterative bilateral filter
#     gray = cv2.bilateralFilter(gray, 11, 17, 17)
    
#     # Perform a dilation and erosion to remove some noise
#     kernel = np.ones((1, 1), np.uint8)
#     gray = cv2.dilate(gray, kernel, iterations=1)
#     gray = cv2.erode(gray, kernel, iterations=1)

#     # Apply threshold to get image with only black and white
#     gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
#             cv2.THRESH_BINARY, 31, 2)
    
#     return gray

# def pdf_to_text(pdf_path):
#     # Convert PDF to images
#     images = convert_from_path(pdf_path)
#     # Process each image
#     for i, image in enumerate(images):
#         # Preprocess the image
#         image = np.array(image)
#         #processed_image = preprocess(image)

#         # Perform OCR on the processed image
#         text = pytesseract.image_to_string(Image.fromarray(image), lang='eng+tel')

#         # Print the OCR outputs
#         print(f'--- Page {i+1} ---')
#         print(text)

def convert(path):
    img=Image.open(path)
    text=pytesseract.image_to_string(img, lang='eng+ori')
    print(text)
    #edit the output file path here
    # Open the file in write mode and write the translated text
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
# Path to your image
image_path = input('Enter the path to the image file: ')
# Path to your output text file
output_path = input('Enter the path to save the output text file: ')
convert(image_path)
# Path to your PDF
# pdf_path = r'converted files\b420043_assignment_11.pdf'

# import os

# # Use os.path.join to form file paths
# file_path = r"C:\Users\Sailesh\Downloads\class-10-sample-paper-2020-21-telugu.pdf"

# try:
#     with open(file_path, 'rb') as f:
#         pdf_to_text(file_path)
#         pass
# except FileNotFoundError:
#     print(f"File not found: {file_path}")
# except PermissionError:
#     print(f"Permission denied: {file_path}")
# except Exception as e:
#     print(f"An error occurred: {e}")
