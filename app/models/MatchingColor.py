import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt


file_path = 'C:\\Users\\Dream4Net\\Desktop\\colors.csv'
colors_df = pd.read_csv(file_path, names=['color', 'color_name', 'hex', 'R', 'G', 'B'])
color_wheel = {
    'Red': ['Yellow', 'Blue', 'Teal'],
    'Green': ['Yellow', 'Blue', 'Teal'],
    'Blue': ['Yellow', 'Red', 'Cyan'],
    'Yellow': ['Red', 'Green', 'Blue'],
    'Teal': ['Red', 'Green', 'Blue'],
    'Cyan': ['Blue', 'Green', 'Purple']
}
def closest_color(color):
    def distance(c1, c2):
        return sum((x - y) ** 2 for x, y in zip(c1, c2))
    
    base_rgb = (color['R'], color['G'], color['B'])
    closest = None
    min_distance = float('inf')
    
    for base_color in color_wheel:
        color_df = colors_df[colors_df['color_name'].str.lower() == base_color.lower()]
        if not color_df.empty:
            base_rgb2 = (color_df['R'].values[0], color_df['G'].values[0], color_df['B'].values[0])
            d = distance(base_rgb, base_rgb2)
            if d < min_distance:
                min_distance = d
                closest = base_color
    
    return closest

def find_matching_color(primary_color_name):
    matching_colors = color_wheel.get(primary_color_name)
    if not matching_colors:
        raise ValueError(f"No matching colors found for {primary_color_name}")
    
    closest_colors = []
    for matching_color in matching_colors:
        matching_color_df = colors_df.query(f'color_name.str.lower() == "{matching_color.lower()}"')
        if not matching_color_df.empty:
            closest_color = matching_color_df.iloc[0]
            closest_colors.append(closest_color)
    
    return closest_colors

def show_colors(primary, matching, second_matching):
    fig, ax = plt.subplots(1, 3, figsize=(15, 5))
    
    ax[0].imshow([[primary['R'], primary['G'], primary['B']]])
    ax[0].set_title(f"Primary Color: {primary['color_name']}")
    ax[0].axis('off')
    
    ax[1].imshow([[matching['R'], matching['G'], matching['B']]])
    ax[1].set_title(f"Matching Color: {matching['color_name']}")
    ax[1].axis('off')
    
    ax[2].imshow([[second_matching['R'], second_matching['G'], second_matching['B']]])
    ax[2].set_title(f"Second Matching Color: {second_matching['color_name']}")
    ax[2].axis('off')
    
    plt.show()

color1 = random.choice(colors_df.to_dict('records'))

matching_color_name = closest_color(color1)

matching_colors = find_matching_color(matching_color_name)

matching_color2 = random.choice(matching_colors)

second_matching_color = colors_df.query(f'color_name.str.lower() == "{matching_color2["color_name"].lower()}"').iloc[0]

show_colors(color1, matching_color2, second_matching_color)