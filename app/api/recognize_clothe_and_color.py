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
from config.cloudinaryConfig import cloudinary
import os
from dotenv import load_dotenv
import onnxruntime as ort


# Load environment variables
load_dotenv()

YOLO_model = os.getenv('YOLO_MODEL_URI')
model = YOLO(YOLO_model)

# Load the color CSV file
Color_cvs = os.getenv('COLOR_URI')
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_df = pd.read_csv(Color_cvs, names=index, header=None)

def load_onnx_model_from_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        model_data = BytesIO(response.content)
        session = ort.InferenceSession(model_data.getvalue())
        return session
    else:
        raise Exception(f"Failed to download model. Status code: {response.status_code}")
# Load ONNX model
onnx_model_url = os.getenv('ONNX_MODEL_URL')
session = load_onnx_model_from_url(onnx_model_url)

# Fabric classification indices and fabric-to-season mapping
class_indices = {0: 'Denim', 1: 'Silk', 2: 'Cotton', 3: 'Wool', 4: 'Leather',
                 5: 'Linen', 6: 'Polyester', 7: 'Rayon', 8: 'Nylon', 9: 'Acrylic',
                 10: 'Spandex', 11: 'Fleece', 12: 'Tweed', 13: 'Velvet', 14: 'Chiffon'}

fabric_to_season = {
    'Denim': ['All seasons'], 'Silk': ['Summer', 'Spring', 'Autumn'],
    'Cotton': ['Summer', 'Spring'], 'Wool': ['Winter', 'Autumn'],
    'Leather': ['Autumn', 'Winter'], 'Linen': ['Summer', 'Spring'],
    'Polyester': ['Spring', 'Autumn'], 'Rayon': ['Spring', 'Summer'],
    'Nylon': ['Spring', 'Autumn'], 'Acrylic': ['Winter', 'Autumn'],
    'Spandex': ['All seasons'], 'Fleece': ['Winter'],
    'Tweed': ['Autumn', 'Winter'], 'Velvet': ['Autumn', 'Winter'],
    'Chiffon': ['Spring', 'Summer']
}

# Preprocessing Functions
def adjust_white_balance(image):
    result = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    avg_a = np.average(result[:, :, 1])
    avg_b = np.average(result[:, :, 2])
    result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
    result = cv2.cvtColor(result, cv2.COLOR_LAB2BGR)
    return result

def adjust_exposure(image, alpha=1.2, beta=0):
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def reduce_noise(image):
    return cv2.medianBlur(image, 5)

def smooth_image(image):
    return cv2.GaussianBlur(image, (5, 5), 0)

def enhance_contrast_clahe(image):
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab_image[:, :, 0] = clahe.apply(lab_image[:, :, 0])
    result = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)
    return result

def preprocess_image(input_image):
    # Remove the background
    image_no_bg = remove(input_image)

    # Convert the image to a format compatible with OpenCV
    image_no_bg_cv = np.array(image_no_bg)
    image_no_bg_cv = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_RGB2BGR)

    # Apply preprocessing steps
    image_no_bg_cv = adjust_white_balance(image_no_bg_cv)
    image_no_bg_cv = reduce_noise(image_no_bg_cv)
    image_no_bg_cv = smooth_image(image_no_bg_cv)
    image_no_bg_cv = enhance_contrast_clahe(image_no_bg_cv)
    image_no_bg_cv = adjust_exposure(image_no_bg_cv)

    # Convert back to PIL for further processing
    processed_image = Image.fromarray(cv2.cvtColor(image_no_bg_cv, cv2.COLOR_BGR2RGB))
    return processed_image

# Fabric classification and season determination
def fabric_seasons(input_image, session):
    img_array = preprocess_image(input_image)
    
    img_array = np.array(img_array.resize((150, 150))).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    
    input_name = session.get_inputs()[0].name
    outputs = session.run(None, {input_name: img_array})
    
    predictions = outputs[0]
    
    if predictions.ndim == 2 and predictions.shape[1] > 0:
        predicted_class_index = np.argmax(predictions, axis=1)[0]
        if predicted_class_index > 14:
            valid_range = range(15)
            predicted_class_index = np.argmax(predictions[0, valid_range])
    else:
        raise ValueError("Unexpected shape for predictions")

    fabric_name = class_indices.get(predicted_class_index, 'Unknown')

    season_order = ["Spring", "Summer", "Autumn", "Winter"]
    season_indicators = [0, 0, 0, 0]

    suitable_seasons = fabric_to_season.get(fabric_name, ['Unknown'])

    for season in suitable_seasons:
        if season == 'All seasons':
            season_indicators = [1, 1, 1, 1]
            break
        if season in season_order:
            index = season_order.index(season)
            season_indicators[index] = 1

    return fabric_name, f"[{','.join(map(str, season_indicators))}]"

# Color palette extraction
def extract_color_palette(image):
    image_cv = np.array(image)
    processed_image = preprocess_image(image_cv)
    
    buffer = BytesIO()
    processed_image.save(buffer, format='JPEG')
    buffer.seek(0)
    
    ct = ColorThief(buffer)
    palette = ct.get_palette(color_count=5)
    hex_colors = ['#%02x%02x%02x' % color for color in palette]
    return hex_colors

# Uploading and processing the image
def upload_image_to_cloudinary(image):
    unique_filename = str(uuid.uuid4())
    result = cloudinary.uploader.upload(image, public_id=unique_filename, overwrite=True, resource_type="image")
    return result['secure_url']

def process_image(input_image):
    image_no_bg = remove(input_image)
    image_no_bg_cv = np.array(image_no_bg)
    image_no_bg_cv = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_RGB2BGR)

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

# Main processing function
def process_and_annotate_image(image_url):
    response = requests.get(image_url)
    input_image = Image.open(BytesIO(response.content))
    
    image_no_bg, label = process_image(input_image)
    fabric_name, seasons = fabric_seasons(input_image, session)
    
    buffer = BytesIO()
    image_no_bg.save(buffer, format="PNG")
    buffer.seek(0)
    
    image_url_no_bg = upload_image_to_cloudinary(buffer)

    hex_colors = extract_color_palette(input_image)
    if label == 'T-shirt':
            label = 'T_shirt'
    result = {
        "image_without_background_url": image_url_no_bg,
        "label": label,
        "color_palette": hex_colors,
        "fabric": fabric_name,
        "seasons": seasons,
    }
    return result
