import pandas as pd
import json
import random
from colorsys import rgb_to_hls
import re

# Helper functions
def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple. Returns None if invalid."""
    if not isinstance(hex_color, str) or not re.match(r'^#[0-9A-Fa-f]{6}$', hex_color):
        return None
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))
    except ValueError:
        return None

def rgb_to_hls_tuple(rgb):
    """Convert RGB tuple to HLS tuple."""
    return rgb_to_hls(rgb[0], rgb[1], rgb[2])

def is_light_color(hex_code, brightness_threshold=0.8):
    """Check if a color is light based on a brightness threshold."""
    rgb = hex_to_rgb(hex_code)
    if rgb is None:
        return False
    r, g, b = rgb
    brightness = (r + g + b) / 3
    return brightness > brightness_threshold

def is_soft_color(hex_code):
    """Check if a color is soft based on HLS values."""
    rgb = hex_to_rgb(hex_code)
    if rgb is None:
        return False
    h, l, s = rgb_to_hls_tuple(rgb)
    # Soft colors typically have high lightness and low saturation
    return l > 0.7 and s < 0.3

def get_color_combination(colors, soft_colors):
    """Create a color combination based on whether soft colors are prioritized."""
    if soft_colors:
        filtered_colors = [color for color in colors if is_soft_color(color)]
        if len(filtered_colors) < 2:
            return filtered_colors
        return random.sample(filtered_colors, 2)
    else:
        return random.sample(colors, 2)

def select_color_for_category(category, colors_list, ids_list, names_list, img_urls_list, categories_list, soft_colors=False):
    """Select a color for a category, prioritizing soft colors if specified."""
    indices = [i for i, cat in enumerate(categories_list) if cat == category]
    if indices:
        category_colors = [colors_list[i] for i in indices]
        color_combination = get_color_combination(category_colors, soft_colors)
        if color_combination:
            color = random.choice(color_combination)
            index = colors_list.index(color)
            return (color, ids_list[index], names_list[index], img_urls_list[index])
    return None

def generate_outfit(json_data, soft_colors=False):
    """Generate an outfit using specified color type (soft or light)."""
    # Extract colors and imgUrl from JSON data
    colors_list, ids_list, names_list, img_urls_list, categories_list = [], [], [], [], []
    for category, subcategories in json_data.items():
        for subcategory, items in subcategories.items():
            for item in items:
                for id_, colors in item.items():
                    img_url = item.get("imgUrl", "")
                    for color in colors:
                        if hex_to_rgb(color) is not None:  # Ensure color is valid
                            colors_list.append(color)
                            ids_list.append(id_)
                            names_list.append(subcategory)
                            img_urls_list.append(img_url)
                            categories_list.append(category)

    # Ensure required categories are present
    required_categories = ["Tops", "Bottoms", "Shoes", "One_Piece"]
    outfit = {}

    # Generate and ensure categories are covered
    for category in required_categories:
        color_info = select_color_for_category(category, colors_list, ids_list, names_list, img_urls_list, categories_list, soft_colors)
        if color_info:
            outfit[category] = color_info

    # Ensure no empty categories
    outfit = {cat: info for cat, info in outfit.items() if info[2]}
    if all(category in outfit and outfit[category][2] for category in ["Tops", "Bottoms", "One_Piece"]):
        selected_category = random.choice(["Tops_Bottoms", "One_Piece"])
        
        if selected_category == "Tops_Bottoms":
            outfit = {cat: outfit[cat] for cat in ["Tops", "Bottoms", "Shoes"] if cat in outfit}
        elif selected_category == "One_Piece":
            outfit = {cat: outfit[cat] for cat in ["One_Piece", "Shoes"] if cat in outfit}

    additional_categories = ["Bags", "Outwear", "Head_wear", "Jewelry"]
    for category in additional_categories:
        if category not in outfit:
            color_info = select_color_for_category(category, colors_list, ids_list, names_list, img_urls_list, categories_list, soft_colors)
            if color_info:
                outfit[category] = color_info

    outfit = {cat: info for cat, info in outfit.items() if info[2]}

    return outfit

def calculate_score(outfit, cleaned_outfits):
    """Calculate the score of an outfit based on its similarity to outfits in cleaned_outfits."""
    scores = [0] * len(cleaned_outfits)  # Fix initialization to match the number of cleaned_outfits

    for idx, row in cleaned_outfits.iterrows():
        score = 0
        if row['Tops'] == outfit.get('Tops', ["", "", "", ""])[2]:
            score += 3
        if row['Bottoms'] == outfit.get('Bottoms', ["", "", "", ""])[2]:
            score += 3
        if row['Shoes'] == outfit.get('Shoes', ["", "", "", ""])[2]:
            score += 3
        if row['One_Piece'] == outfit.get('One_Piece', ["", "", "", ""])[2]:
            score += 6
        if row['Bags'] == outfit.get('Bags', ["", "", "", ""])[2]:
            score += 2
        if row['Outwear'] == outfit.get('Outwear', ["", "", "", ""])[2]:
            score += 2
        if row['Head_wear'] == outfit.get('Head_wear', ["", "", "", ""])[2]:
            score += 1
        if row['Jewelry'] == outfit.get('Jewelry', ["", "", "", ""])[2]:
            score += 1
        
        scores[idx] = score  # Store the score for the outfit at this index

    return scores

def get_top_outfits(outfits, cleaned_outfits):
    """Calculate scores for all outfits and return the top 3."""
    scored_outfits = [(outfit, max(calculate_score(outfit, cleaned_outfits))) for outfit in outfits]
    top_outfits = sorted(scored_outfits, key=lambda x: x[1], reverse=True)[:3]
    return top_outfits

def final_outfits(json_data):
    # Load data and generate outfits
    cleaned_outfits = pd.read_csv('C:\\Users\\Dream4Net\\Desktop\\images_outfits\\outfits_final_summer.csv')
   

    # Generate 6 outfits using different color criteria
    outfits = []
    outfits.extend([generate_outfit(json_data, soft_colors=False) for _ in range(3)])  # Light color outfits
    outfits.extend([generate_outfit(json_data, soft_colors=True) for _ in range(3)])  # Soft color outfits

    # Ensure that none of the outfits are None (invalid)
    outfits = [outfit for outfit in outfits if outfit is not None]

    # Get top 3 outfits based on the score
    top_outfits = get_top_outfits(outfits, cleaned_outfits)

    # Format top outfits as JSON
    formatted_outfits = []
    for i, (outfit, score) in enumerate(top_outfits, start=1):
        formatted_outfit = {"Outfit": i}

        # Add categories only if they are not empty
        for category in ["Tops", "Bottoms", "Shoes", "One_Piece", "Bags", "Outwear", "Head_wear", "Jewelry"]:
            item = outfit.get(category, ["", "", "", ""])
            if item[2]:
                formatted_outfit[category] = {
                    "name": item[2],
                    "id": item[1],
                    "imgUrl": item[3]
                }

        formatted_outfits.append(formatted_outfit)
    return formatted_outfits
