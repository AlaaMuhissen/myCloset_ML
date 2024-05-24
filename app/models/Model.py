import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
import pandas as pd
import os

class FashionMNISTModel:
    def __init__(self, model_path, feedback_path, train_path):
        self.model_path = model_path
        self.feedback_path = feedback_path
        self.train_path = os.path.abspath(train_path)
        self.model = tf.keras.models.load_model(model_path)
        self.feedback_data = self.load_dataset(feedback_path)

    def load_dataset(self, path):
        if os.path.exists(path):
            return pd.read_csv(path)
        else:
            return pd.DataFrame(columns=["label"] + [f"pixel{i}" for i in range(1, 785)])

    def save_dataset(self, path, data):
        data.to_csv(path, index=False)

    def update_model(self, new_images, new_labels):
       
        new_labels = tf.keras.utils.to_categorical(new_labels, num_classes=10)
        self.model.fit(new_images, new_labels, epochs=5, validation_split=0.2)
        self.model.train_on_batch(new_images, new_labels)
        self.model.save(self.model_path)

    def update_train_data(self, rows_to_move=5):
        train_data = pd.read_csv(self.train_path)
        feedback_rows = self.feedback_data.head(rows_to_move)
        train_data = pd.concat([train_data, feedback_rows], ignore_index=True)
        train_data.to_csv(self.train_path, index=False, mode='w', header=True) 
        self.feedback_data = self.feedback_data.iloc[rows_to_move:, :]
        self.save_dataset(self.feedback_path, self.feedback_data)




    def process_image(self, image_path):
        new_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        new_image = cv2.resize(new_image, (28, 28))
        new_image = new_image.reshape((1, 28, 28, 1)).astype('float32') / 255.0
        return new_image

    def predict_image(self, new_image):
        predicted_label = self.model.predict(new_image)
        predicted_class = np.argmax(predicted_label)
        return predicted_class

    def interact_with_user(self):
        while True:
            image_path = input("Enter the path of a new Fashion MNIST image (or 'exit' to quit): ")
            if image_path.lower() == 'exit':
                break

            new_image = self.process_image(image_path)
            predicted_class = self.predict_image(new_image)

            plt.imshow(new_image.reshape(28, 28), cmap='gray')
            plt.title(f"Predicted: {predicted_class}")
            plt.axis('off')
            plt.show()

            user_response = input("Is the prediction correct? (yes/no): ").lower()

            if user_response == "no":
                correct_label = input("Please provide the correct label for the Fashion MNIST image: ")
                self.feedback_data = pd.concat([self.feedback_data,
                                               pd.DataFrame([{"label": int(correct_label) if correct_label else predicted_class,
                                                              **{f"pixel{i}": val for i, val in enumerate(new_image.reshape(-1), start=1)}}])],
                                              ignore_index=True)
                self.save_dataset(self.feedback_path, self.feedback_data)

                if len(self.feedback_data) >= 5:
                    new_images = self.feedback_data.iloc[:, 1:].values.reshape(-1, 28, 28, 1)
                    new_labels = self.feedback_data["label"].values

                    new_images = new_images.astype('float32') / 255.0
                    self.update_model(new_images, new_labels)
                    self.update_train_data() 

                    print("Model updated!")

        print("Thank you for your feedback!")

fashion_mnist_model = FashionMNISTModel("fashion_mnist_model.keras", "feedback_data.csv", "fashion-mnist_train.csv")
fashion_mnist_model.interact_with_user()
