import requests
from io import BytesIO
from ultralytics import YOLO
from rembg import remove
from PIL import Image
import cv2
import numpy as np
import pandas as pd
from colorthief import ColorThief
import cloudinary.uploader
import uuid
from config import cloudinary

# Load the YOLO model once
model = YOLO('https://regognize-clothes-model.s3.eu-west-1.amazonaws.com/regognizeClothesModel.pt')

# Read the colors CSV file once
csv_path = 'https://regognize-clothes-model.s3.eu-west-1.amazonaws.com/colors.csv'
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_df = pd.read_csv(csv_path, names=index, header=None)

def upload_image_to_cloudinary(image):
    unique_filename = str(uuid.uuid4())
    result = cloudinary.uploader.upload(image, public_id=unique_filename, overwrite=True, resource_type="image")
    return result['secure_url']

def process_image(input_image):
    # Remove the background
    image_no_bg = remove(input_image)

    # Convert the image to a format compatible with OpenCV
    image_no_bg_cv = np.array(image_no_bg)
    image_no_bg_cv = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_RGB2BGR)

    # Perform object detection
    results = model(image_no_bg)
    resultss = results[0].boxes.data.cpu().numpy()

    label = None
    for result in resultss:
        xmin, ymin, xmax, ymax, score, class_id = result
        label = model.names[int(class_id)]
        confidence = score
        cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)
        text = f'{label} {confidence:.2f}'
        (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
        cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin) - text_height - 10), (int(xmin) + text_width, int(ymin)), (255, 0, 0), -1)
        cv2.putText(image_no_bg_cv, text, (int(xmin), int(ymin) - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

    return image_no_bg, label

def extract_color_palette(image):
    # Extract the color palette from the input image
    ct = ColorThief(image)
    palette = ct.get_palette(color_count=5)
    hex_colors = ['#%02x%02x%02x' % color for color in palette]
    return hex_colors

def process_and_annotate_image(input_image_bytes):
    input_image = Image.open(BytesIO(input_image_bytes))
    image_no_bg, label = process_image(input_image)
    color_palette = extract_color_palette(BytesIO(input_image_bytes))
    
    # Convert the image to a format suitable for upload
    buffer = BytesIO()
    image_no_bg.save(buffer, format="PNG")
    image_data = buffer.getvalue()
    
    # Upload the image to Cloudinary and get the URL
    image_url = upload_image_to_cloudinary(image_data)
    
    return {
        "image_without_background_url": image_url,
        "label": label,
        "color_palette": color_palette
    }
