import pandas as pd
import matplotlib.pyplot as plt
from colorthief import ColorThief
import easygui
import cv2
from rembg import remove
from PIL import Image
import os
#Simulation of remove background,analyze color and save them
csv_path = '.\colors.csv'
index = ['color', 'color_name', 'hex', 'R', 'G', 'B']

color_df = pd.read_csv(csv_path, names=index, header=None)

def capture_image():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cv2.imwrite("captured_image.png", frame)
    cap.release()

def select_image():
    image_path = easygui.fileopenbox(title='Select image file')
    return image_path

def get_image_path():
    choice = easygui.buttonbox("Choose image source", choices=["Camera", "Library"])
    if choice == "Camera":
        capture_image()
        return "captured_image.png"
    elif choice == "Library":
        return select_image()
    else:
        return None

def create_color_images_folder():
    output_folder = 'color_images'
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder

image_path = get_image_path()

if not image_path:
    print("No image selected or captured. Exiting...")
    exit()

input_image = Image.open(image_path)
output_image = remove(input_image)

outputpath = easygui.filesavebox(title='Save file to ', default='output.png', filetypes=['*.png', '*.jpg', '*.jpeg'])

if not outputpath:
    print("No output file selected. Exiting...")
    exit()

output_image_format = outputpath.split('.')[-1].upper()  
output_image.save(outputpath, format=output_image_format)

ct = ColorThief(outputpath)
palette = ct.get_palette(color_count=3)

output_folder = create_color_images_folder()

for color in palette:
    closest_color = color_df.iloc[(color_df[['R', 'G', 'B']] - color).pow(2).sum(1).idxmin()]
    color_name = closest_color['color_name']
    color_image = Image.new("RGB", (100, 100), color)
    color_image_path = os.path.join(output_folder, f"{color_name}.png")
    color_image.save(color_image_path)

# Display color images
fig, axs = plt.subplots(1, len(palette) + 1, figsize=(15, 3))

for i, color in enumerate(palette):
    closest_color = color_df.iloc[(color_df[['R', 'G', 'B']] - color).pow(2).sum(1).idxmin()]
    color_name = closest_color['color_name']
    
    axs[i].imshow([[color]])
    axs[i].set_title(f"{color_name}\nRGB: {color}")
    axs[i].axis('off')

axs[-1].axis('off')

plt.tight_layout()
plt.show()
