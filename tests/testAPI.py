import requests

# URL of the FastAPI endpoint
url = "http://127.0.0.1:8000/recognize-clothes-and-colors/"

# URL of the image to be tested
image_url = 'https://firebasestorage.googleapis.com/v0/b/mycloset-c256e.appspot.com/o/Clothes%2FIMG_0850.jpeg?alt=media&token=ca2e2ecd-e7e4-4738-b1c8-57dceaab8f95' # Replace with an actual image URL

# Prepare the data to be sent in the POST request
data = {
    "image_url": image_url
}

# Send the POST request with the image URL
response = requests.post(url, data=data)

# Check the response
if response.status_code == 200:
    print("Image processed successfully:")
    print(response.json())
else:
    # Print the error message
    print(f"Failed to process image: {response.status_code}, {response.text}")
