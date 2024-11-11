# 🧠 myCloset Machine Learning (ML)

Welcome to the **myCloset Machine Learning** repository! This repository contains the ML models, API, and algorithms that power the *myCloset* fashion app’s advanced clothing and color recognition features. Developed with **Python** and **FastAPI**, this component enables the app to analyze, tag, and classify wardrobe items, providing users with personalized outfit suggestions based on factors like temperature, occasion, and clothing compatibility.

- 🔗 **Backend Repository**: [myCloset Backend](https://github.com/AlaaMuhissen/myCloset_backend)
- 🔗 **Frontend Repository**: [myCloset Frontend](https://github.com/AlaaMuhissen/myCloset_frontend)


## 📂 Repository Structure
- **app/** - Contains the FastAPI application code, endpoint definitions, and model integrations.
- **config/** - Configuration files for setting model parameters and environment variables.
- **data/** - Folder for storing training and test datasets.
- **models/** - Includes the pre-trained models for clothing recognition, color extraction, and fabric detection.
- **tests/** - Scripts and sample data for testing model performance and endpoint responses.
- **main.py** - Main entry point for running the FastAPI server.
- **recognizeClothesModel.pt** - The pre-trained PyTorch model for clothing recognition.
- **Dockerfile** and **docker-compose.yml** - Configurations for containerizing the FastAPI app and ML models.

## 🧰 Features
- **FastAPI Endpoints**: Exposes endpoints to interact with the ML models for clothing and color recognition, enabling seamless integration with the frontend.
- **Clothing Recognition**: Detects and categorizes clothing items in images, identifying types like tops, bottoms, shoes, and accessories using a custom-trained model.
- **Color Detection**: Extracts prominent colors from clothing items, helping to tag and organize wardrobe items by color.
- **Fabric Detection**: Identifies fabric types (e.g., cotton, wool, silk) to allow filtering and better outfit selection based on fabric properties.
- **Clothes-Matching Algorithm**: Suggests cohesive outfits by analyzing clothing type, color harmony, temperature, and occasion, creating versatile options for users.
- **Model Training and Testing**: Scripts to retrain and evaluate model performance, ensuring continuous improvement with new data.

## 🧑‍💻 Models Used
- **YOLOv5 (You Only Look Once)**: A pre-trained YOLOv5 model, fine-tuned for clothing detection and classification. YOLO provides accurate, real-time object detection, ideal for identifying clothing items within images.
- **Color Clustering (K-means)**: K-means clustering is used for color detection, identifying dominant colors in clothing items by clustering pixel colors within the image.
- **Fabric Classification Model**: A custom model that classifies fabric types based on texture patterns and other image features, enhancing filtering options for users.

## 👗 Clothes-Matching Algorithm
The clothes-matching algorithm generates outfits by combining key factors to create visually cohesive and contextually appropriate suggestions. It considers:
- **Clothing Type Compatibility**: Ensures essential items (e.g., top, bottom, shoes) are included in each outfit.
- **Color Harmony**: Uses color theory principles to select complementary or analogous colors.
- **Temperature and Occasion**: Adjusts outfit suggestions based on the current temperature and the occasion, ensuring both style and comfort.
  
The algorithm generates two outfit variations—one prioritizing bright colors and another with softer tones—saved in JSON format for easy retrieval by the frontend.

## 🚀 Technologies
- **Python** - Core programming language for ML model development.
- **FastAPI** - Framework for creating the API endpoints that interact with the models.
- **PyTorch** - Deep learning framework for training and running the YOLOv5 clothing recognition model.
- **OpenCV** - Used for image preprocessing and color extraction.
- **Docker** - Containerization for consistent and portable deployment of the FastAPI app and ML models.

## ⚙️ Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AlaaMuhissen/myCloset_ML.git
   cd myCloset_ML
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI App**
   Start the FastAPI server to expose the endpoints:
   ```bash
   uvicorn main:app --reload
   ```

4. **Using Docker**
   To run the entire application in a Docker container:
   ```bash
   docker-compose up --build
   ```

## 📡 API Endpoints

- **`POST /recognize-clothes/`**: Accepts an image input and returns detected clothing types with bounding boxes.
- **`POST /detect-colors/`**: Accepts an image input and returns the dominant colors of the clothing items.
- **`POST /detect-fabric/`**: Accepts an image input and returns the detected fabric type.
- **`POST /match-outfit/`**: Generates a recommended outfit based on input preferences, including temperature, occasion, and selected items.

## 🔬 Testing
Use the `tests/` directory to test model performance and API endpoints with sample data:
   ```bash
   python -m unittest discover -s tests
   ```

## 🤝 Contributing
Contributions are welcome! To contribute:
1. **Fork** this repository.
2. **Create a branch**: `git checkout -b feature-name`
3. **Commit your changes**: `git commit -m 'Add new feature'`
4. **Push the branch**: `git push origin feature-name`
5. **Open a Pull Request**
