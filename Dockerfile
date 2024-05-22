# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && apt-get clean
# Copy the current directory contents into the container at /app
COPY requirements.txt /app/
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80 

# Define environment variable
ENV NAME World

# Run recognizeClotheAndColor.py when the container launches
CMD ["python", "recognize-clothe-and-color.py"]
