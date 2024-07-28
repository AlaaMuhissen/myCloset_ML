import random
import json
from colorsys import rgb_to_hls

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def rgb_to_hls_tuple(rgb):
    return rgb_to_hls(rgb[0], rgb[1], rgb[2])

def is_light_color(hex_code, brightness_threshold=200):
    r, g, b = hex_to_rgb(hex_code)
    brightness = (r + g + b) / 3
    return brightness > brightness_threshold

def is_soft_color(hex_code):
    rgb = hex_to_rgb(hex_code)
    h, l, s = rgb_to_hls_tuple(rgb)
    return l > 0.7 and s < 0.3

def get_soft_color_combination(colors):
    soft_colors_list = [color for color in colors if is_soft_color(color)]
    if len(soft_colors_list) < 2:
        return soft_colors_list
    return random.sample(soft_colors_list, 2)

def select_color_for_category(category, colors_list, ids_list, names_list, categories_list, soft_colors=False):
    indices = [i for i, cat in enumerate(categories_list) if cat == category]
    if indices:
        category_colors = [colors_list[i] for i in indices]
        if soft_colors:
            soft_combination = get_soft_color_combination(category_colors)
            if soft_combination:
                color = random.choice(soft_combination)
            else:
                color = random.choice(category_colors)
        else:
            color = random.choice(category_colors)
        index = colors_list.index(color)
        return { "name": names_list[index], "id": ids_list[index]}
    return None

def generate_outfit(json_data, soft_colors=False):
    colors_list, ids_list, names_list, categories_list = [], [], [], []
    for category, subcategories in json_data.items():
        for subcategory, items in subcategories.items():
            for item in items:
                for id_, colors in item.items():
                    for color in colors:
                        colors_list.append(color)
                        ids_list.append(id_)
                        names_list.append(subcategory)
                        categories_list.append(category)

    required_categories = ["Tops", "Bottoms", "Shoes", "Bags", "Accessories"]
    outfit = {}
    
    selected_ids = set()  
    
    for category in required_categories:
        color_info = select_color_for_category(category, colors_list, ids_list, names_list, categories_list, soft_colors)
        if color_info and color_info['id'] not in selected_ids:
            outfit[category] = color_info
            selected_ids.add(color_info['id'])

    return outfit

api_url = " " 
response = requests.get(api_url)
json_data = response.json()
light_outfit = generate_outfit(json_data, soft_colors=False)
soft_outfit = generate_outfit(json_data, soft_colors=True)

output_data = {
    "OUTFIT_1 ": light_outfit,
    "OUTFIT_2": soft_outfit
}

with open('outfits.json', 'w') as outfile:
    json.dump(output_data, outfile, indent=4)
