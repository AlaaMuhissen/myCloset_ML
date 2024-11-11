# 🧠 myCloset Machine Learning (ML)

Welcome to the **myCloset Machine Learning** repository! This repository contains the ML models and API code that power the *myCloset* fashion app’s advanced clothing and color recognition features. Developed with **Python** and **FastAPI**, this component enables the app to analyze, tag, and classify wardrobe items, enhancing the user experience with intelligent insights.

## 📂 Repository Structure
- **app/** - Contains the FastAPI application code, endpoint definitions, and model integrations.
- **config/** - Configuration files for setting model parameters and environment variables.
- **data/** - Folder for storing training and test datasets.
- **models/** - Includes the pre-trained models for clothing recognition and color extraction.
- **tests/** - Scripts and sample data for testing model performance and endpoint responses.
- **main.py** - Main entry point for running the FastAPI server.
- **recognizeClothesModel.pt** - The pre-trained PyTorch model for clothing recognition.
- **Dockerfile** and **docker-compose.yml** - Configurations for containerizing the FastAPI app and ML models.

## 🧰 Features
- **FastAPI Endpoints**: Exposes endpoints to interact with the ML models for clothing and color recognition, enabling seamless integration with the frontend.
- **Clothing Recognition**: Detects and categorizes clothing items in images, identifying types like tops, bottoms, shoes, and accessories using a custom-trained model.
- **Color Detection**: Extracts prominent colors from clothing items, helping to tag and organize wardrobe items by color.
- **Model Training and Testing**: Scripts to retrain and evaluate model performance, ensuring continuous improvement with new data.

## 🧑‍💻 Models Used
- **YOLOv5 (You Only Look Once)**: A pre-trained YOLOv5 model, fine-tuned for clothing detection and classification. YOLO provides accurate, real-time object detection, ideal for identifying clothing items within images.
- **Color Clustering (K-means)**: K-means clustering is used for color detection, identifying dominant colors in clothing items by clustering pixel colors within the image.

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
  
These endpoints enable seamless integration with the frontend, allowing for real-time clothing and color recognition.

## 🤝 Contributing
Contributions are welcome! To contribute:
1. **Fork** this repository.
2. **Create a branch**: `git checkout -b feature-name`
3. **Commit your changes**: `git commit -m 'Add new feature'`
4. **Push the branch**: `git push origin feature-name`
5. **Open a Pull Request**
