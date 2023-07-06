import cv2
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import numpy as np

import cv2
import numpy as np
import uuid

# Adding custom options
custom_config = r'--oem 3 --psm 1'

def clean_image(image):

     def HSV_mask(img_hsv, lower):
          lower = np.array(lower)
          upper = np.array([255, 255, 255])
          return cv2.inRange(img_hsv, lower, upper)
     
     # img = cv2.imread("/home/srihari/Desktop/water_mark_issue/im/Gwalior_HC_page-0001.jpg")
     img = image

     img_hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

     img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)


     img_gray[img_gray >= 220] = 255

     mask1 = HSV_mask(img_hsv, [0, 0, 155])[..., None].astype(np.float32)

     mask2 = HSV_mask(img_hsv, [0, 20, 0])
     masked = np.uint8((img + mask1) / (1 + mask1 / 255))



     gray = cv2.cvtColor(masked, cv2.COLOR_RGB2GRAY)
     gray[gray >= 175] = 255


     gray[mask2 == 0] = img_gray[mask2 == 0]

     # clean = clean_image(gray)
     gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

     image_id=str(uuid.uuid4())
     return gray




def pdf_to_text(pdf_path, language):
    # Convert PDF to images
    images = convert_from_path(pdf_path)

    # Process each image
    for i, image in enumerate(images):
        # Preprocess the image
        if (i>=0):

            image = np.array(image)
            #processed_image = preprocess(image)
            # # Perform OCR on the processed image
            text = pytesseract.image_to_string((clean_image(image)), lang=f'{language}')

            # Print the OCR outputs
            print(f'--- Page {i+1} ---')
            print(text)
            with open(output_path, 'a', encoding='utf-8') as f:
                f.write(f'--- Page {i+1} ---')
                f.write(text)

def convert(path):
    img=Image.open(path)
    img=np.array(img)
    #print(img)
    text=pytesseract.image_to_string(clean_image(img), lang='ori')
    print(text)
    #edit the output file path here
    # Open the file in write mode and write the translated text
    with open(output_path, 'w',encoding='UTF-8') as f:
        f.write(text)

# Path to your pdf
file_path = input('Enter the path to the PDF file: ')
# Path to your output text file
output_path = input('Enter the path to save the output text file: ')
print('\nSelect the language:')
print('For Telugu Type: tel')
print('For English Type: eng')
print('For Oriya Type: ori\n')

language = input('Enter the Input language of the pdf\n')

#convert(file_path,language)

try:
    with open(file_path, 'rb') as f:
        pdf_to_text(file_path,language)
        pass
except FileNotFoundError:
    print(f"File not found: {file_path}")
except PermissionError:
    print(f"Permission denied: {file_path}")
except Exception as e:
    print(f"An error occurred: {e}")

