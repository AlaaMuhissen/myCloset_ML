from ultralytics import YOLO
from rembg import remove
import easygui
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import pandas as pd
from colorthief import ColorThief
import matplotlib.pyplot as plt

inputpath = easygui.fileopenbox(title='Select image file')
outputpath = easygui.filesavebox(title='Save file to ')

input_image = Image.open(inputpath)
image_no_bg = remove(input_image)
image_no_bg_cv = np.array(image_no_bg)
image_no_bg_cv = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_RGB2BGR)
model = YOLO('C:\\Users\\Dream4Net\\Desktop\\best.pt')
results = model(image_no_bg)
resultss = results[0].boxes.data.cpu().numpy()
for result in resultss:
    xmin, ymin, xmax, ymax, score, class_id = result
    label = model.names[int(class_id)]
    confidence = score
    cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin)), (int(xmax), int(ymax)), (255, 0, 0), 2)
    text = f'{label} {confidence:.2f}'
    (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3) 
    cv2.rectangle(image_no_bg_cv, (int(xmin), int(ymin) - text_height - 10), (int(xmin) + text_width, int(ymin)), (255, 0, 0), -1)
    cv2.putText(image_no_bg_cv, text, (int(xmin), int(ymin) - 5), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)  # Adjusted font scale and thickness

csv_path = 'C:\\Users\\Dream4Net\\Desktop\\colors.csv'
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_df = pd.read_csv(csv_path, names=index, header=None)

ct = ColorThief(inputpath)
palette = ct.get_palette(color_count=5)

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

image_no_bg_rgb = cv2.cvtColor(image_no_bg_cv, cv2.COLOR_BGR2RGB)
image_no_bg_pil = Image.fromarray(image_no_bg_rgb)

width, height = image_no_bg_pil.size
new_width = width + 200  
new_height = height
new_image = Image.new('RGB', (new_width, new_height), (255, 255, 255)) 
new_image.paste(image_no_bg_pil, (0, 0))

draw = ImageDraw.Draw(new_image)
# Load a larger font
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
new_image.save(outputpath)
print(f'Result image saved to {outputpath}')

plt.figure(figsize=(10, 10)) 
plt.imshow(new_image)
plt.axis('off')  
plt.show()
