import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
model = tf.keras.models.load_model('fabric24_model.keras')
class_indices = {
    0: 'Denim',
    1: 'Silk',
    2: 'Cotton',
    3: 'Wool',
    4: 'Leather',
    5: 'Linen',
    6: 'Polyester',
    7: 'Rayon',
    8: 'Nylon',
    9: 'Acrylic',
    10: 'Spandex',
    11: 'Fleece',
    12: 'Tweed',
    13: 'Velvet',
    14: 'Chiffon'
}
fabric_to_season = {
    'Denim': ['Autumn', 'Winter'],
    'Silk': ['Summer', 'Spring', 'Autumn'],
    'Cotton': ['Summer', 'Spring'],
    'Wool': ['Winter', 'Autumn'],
    'Leather': ['Autumn', 'Winter'],
    'Linen': ['Summer', 'Spring'],
    'Polyester': ['Spring', 'Autumn'],
    'Rayon': ['Spring', 'Summer'],
    'Nylon': ['Spring', 'Autumn'],
    'Acrylic': ['Winter', 'Autumn'],
    'Spandex': ['All seasons'], 
    'Fleece': ['Winter'],
    'Tweed': ['Autumn', 'Winter'],
    'Velvet': ['Autumn', 'Winter'],
    'Chiffon': ['Spring', 'Summer']
}

def preprocess_image(img_path, target_size=(150, 150)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def predict_image_class(img_path, model):
    img_array = preprocess_image(img_path)
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    return predicted_class

def get_fabric_name(class_index):
    return class_indices.get(class_index, 'Unknown')

def get_suitable_seasons(fabric_name):
    return fabric_to_season.get(fabric_name, 'Unknown')
img_path = 'C:\\Users\\Dream4Net\\Desktop\\qw\\jeans15.jpg'  
predicted_class = predict_image_class(img_path, model)
fabric_name = get_fabric_name(predicted_class)
suitable_seasons = get_suitable_seasons(fabric_name)

print(f'Predicted class index: {predicted_class}')
print(f'Predicted fabric type: {fabric_name}')
print(f'Suitable seasons for {fabric_name}: {", ".join(suitable_seasons)}')
