import sys
import requests
from io import BytesIO
from ultralytics import YOLO
from rembg import remove
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import pandas as pd
from colorthief import ColorThief
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
    print("Usage: python recognize-clothe-and-color.py <input_image_url> <output_image_path>")
    sys.exit(1)

input_url = sys.argv[1]
outputpath = sys.argv[2]

# Download the image from the URL
response = requests.get(input_url)
if response.status_code == 200:
    input_image = Image.open(BytesIO(response.content))
else:
    print(f"Failed to download image. Status code: {response.status_code}")
    sys.exit(1)

# Remove the background
image_no_bg = remove(input_image)

# Convert the image to a format compatible with OpenCV
image_no_bg_cv = np.array(image_no_bg)
image_no_bg_cv = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_RGB2BGR)

# Load the YOLO model
model = YOLO('https://regognize-clothes-model.s3.eu-west-1.amazonaws.com/regognizeClothesModel.pt')

# Perform object detection
results = model(image_no_bg)
resultss = results[0].boxes.data.cpu().numpy()

# Draw bounding boxes and labels on the image
for result in resultss:
    xmin, ymin, xmax, ymax, score, class_id = result
    label = model.names[int(class_id)]
    confidence = score
    cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)
    text = f'{label} {confidence:.2f}'
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)
    cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin) - text_height - 10), (int(xmin) + text_width, int(ymin)), (255, 0, 0), -1)
    cv2.putText(image_no_bg_cv, text, (int(xmin), int(ymin) - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

# Read the colors CSV file
csv_path = 'https://regognize-clothes-model.s3.eu-west-1.amazonaws.com/colors.csv'
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_df = pd.read_csv(csv_path, names=index, header=None)

# Extract the color palette from the input image
ct = ColorThief(BytesIO(response.content))
palette = ct.get_palette(color_count=5)

# Display the color palette
fig, axs = plt.subplots(1, len(palette) + 1, figsize=(15, 3))
for i, color in enumerate(palette):
    closest_color = color_df.iloc[(color_df[['R', 'G', 'B']] - color).pow(2).sum(1).idxmin()]
    color_name = closest_color['color_name']
    axs[i].imshow([[color]])
    axs[i].set_title(color_name)
    axs[i].axis('off')
axs[-1].axis('off')
plt.tight_layout()
plt.show()

# Convert the image back to a format compatible with PIL
image_no_bg_rgb = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_BGR2RGB)
image_no_bg_pil = Image.fromarray(image_no_bg_rgb)

# Create a new image with additional space for labels
width, height = image_no_bg_pil.size
new_width = width + 200
new_height = height
new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255))
new_image.paste(image_no_bg_pil, (0, 0))

# Draw labels on the new image
draw = ImageDraw.Draw(new_image)
try:
    font = ImageFont.truetype("arial.ttf", 20)
except IOError:
    font = ImageFont.load_default()

text_start_y = 10
for result in resultss:
    _, _, _, _, _, class_id = result
    label = model.names[int(class_id)]
    draw.text((width + 10, text_start_y), f'Label: {label}', fill=(0, 0, 0), font=font)
    text_start_y += 30

for i, color in enumerate(palette):
    closest_color = color_df.iloc[(color_df[['R', 'G', 'B']] - color).pow(2).sum(1).idxmin()]
    color_name = closest_color['color_name']
    draw.text((width + 10, text_start_y), f'Color: {color_name}', fill=(0, 0, 0), font=font)
    text_start_y += 30

# Save the resulting image
new_image.save(outputpath)
print(f'Result image saved to {outputpath}')

# Display the resulting image
plt.figure(figsize=(10, 10))
plt.imshow(new_image)
plt.axis('off')
plt.show()
