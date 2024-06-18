import requests

# URL of the FastAPI endpoint
url = "http://127.0.0.1:8000/"

# URL of the image to be tested
image_url = 'https://res.cloudinary.com/depgto6ws/image/upload/v1718708768/ppbyspzdmeecgrq8k18l.jpg' # Replace with an actual image URL

# Prepare the data to be sent in the POST request
data = {
    "image_url": image_url
}

# Send the POST request with the image URL
response = requests.get(url)

# Check the response
if response.status_code == 200:
    print("Image processed successfully:")
    print(response.json())
else:
    # Print the error message
    print(f"Failed to process image: {response.status_code}, {response.text}")
