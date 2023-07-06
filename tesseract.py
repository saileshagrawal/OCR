from PIL import Image
from pdf2image import convert_from_path
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter import messagebox

import numpy as np
import cv2
import tkinter
# import pytesseract
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




def pdf_to_text(pdf_path, output_path, language):
    # Convert PDF to images
    print(pdf_path, output_path, language)
    images = convert_from_path(pdf_path, output_path)

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

def convert(path, output_path):
    img=Image.open(path)
    img=np.array(img)
    #print(img)
    text=pytesseract.image_to_string(clean_image(img), lang='ori')
    print(text)
    #edit the output file path here
    # Open the file in write mode and write the translated text
    with open(output_path, 'w',encoding='UTF-8') as f:
        f.write(text)


def main(file_path, output_path, language):
    output_path = output_path + "/" + file_path.split("/")[-1].split(".")[0] + ".txt"
    print(file_path, output_path, language)
    try:
        with open(file_path, 'rb') as f:
            pdf_to_text(file_path, output_path, language)
            pass
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {file_path}")
    except PermissionError:
        messagebox.showerror("Error", "Permission denied")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# File selection button
def file_selection(selection):
    if selection == "input":
        file_path = askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        input_file_selection_button.config(text=file_path)
    elif selection == "output":
        output_path = askdirectory()
        output_file_selection_button.config(text=output_path)

# Tkinter app to accept file_path, output_path and langugae dropdown

root = tkinter.Tk()
root.title("PDF to Text")
# root.geometry("500x300")

# Create a Tkinter variable
tkvar = tkinter.StringVar(root)

# Dictionary with options
choices = { 'tel','eng','ori'}
tkvar.set('tel') # set the default option

popupMenu = tkinter.OptionMenu(root, tkvar, *choices)
tkinter.Label(root, text="Choose a language").grid(row = 0, column = 0)
popupMenu.grid(row = 0, column =1)

intpu_file_path_label = tkinter.Label(root, text="Select Input file: ")
intpu_file_path_label.grid(row=1, column=0)

input_file_selection_button = tkinter.Button(root, text="--Select--", command=lambda : file_selection("input"))
input_file_selection_button.grid(row=1, column=1)

output_file_path_label = tkinter.Label(root, text="Select Output Folder: ")
output_file_path_label.grid(row=2, column=0)

output_file_selection_button = tkinter.Button(root, text="--Select--", command=lambda : file_selection("output"))
output_file_selection_button.grid(row=2, column=1)

submit_button = tkinter.Button(root, text="Submit", command=lambda : main(input_file_selection_button.cget("text"), output_file_selection_button.cget("text"), tkvar.get()))
submit_button.grid(row=3, column=1)

root.mainloop()







