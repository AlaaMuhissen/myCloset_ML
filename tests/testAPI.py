import os
import requests

url = "http://127.0.0.1:8000/recognize-clothes-and-colors/"

# Get the base directory of the project
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_dir, 'data', 'sample_images', 'watch.jpeg')

with open(file_path, "rb") as f:
    files = {"file": ("watch.jpeg", f)}
    response = requests.post(url, files=files)

if response.status_code == 200:
    with open("output_image.jpg", "wb") as out:
        out.write(response.content)
    print("Processed image saved as output_image.jpg")
else:
    print(f"Failed to process image: {response.status_code}")
