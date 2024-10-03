# recommender.py

import numpy as np
import tensorflow as tf
from data import products  # Ensure your products list is imported correctly

class RecommendationSystem:
    def __init__(self):
        self.products = products
        self.model = self.build_model()
        self.train_model()

    def build_model(self):
        # Build a simple model to recommend products based on user interactions
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(2,)),  # Input for user and product indices
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(len(self.products), activation='softmax')  # Output layer size must match product count
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def prepare_data(self):
        # Prepare dummy training data
        user_ids = []
        product_ids = []
        for i, product in enumerate(self.products):
            user_ids.append(0)  # Dummy user index
            product_ids.append(product['id'])  # Product id as label

        return np.array(user_ids), np.array(product_ids)

    def train_model(self):
        user_ids, product_ids = self.prepare_data()
        # Fit the model with user-product pairs
        # The product_ids must match the indices of the products
        self.model.fit(np.array(list(zip(user_ids, product_ids))), product_ids, epochs=50)  # Increase epochs if needed

    def recommend_by_category(self, category, temperature=1.0, num_recommendations=2):
        # Generate recommendations for a given category
        category_products = [product for product in self.products if product['category'] == category]

        if not category_products:
            return []

        # Prepare input for the model
        product_indices = [p['id'] for p in category_products]
        user_indices = np.zeros(len(product_indices))  # Dummy user index

        # Make predictions
        predictions = self.model.predict(np.array(list(zip(user_indices, product_indices))))

        # Apply temperature scaling to the predictions
        scaled_predictions = predictions / temperature  # Scale predictions by temperature
        softmax_predictions = tf.nn.softmax(scaled_predictions).numpy()  # Get softmax probabilities

        # Get the corresponding softmax predictions for the category products
        softmax_probs = softmax_predictions[0][:len(category_products)]

        # Sample from the softmax distribution
        recommended_indices = np.random.choice(len(category_products), size=num_recommendations, p=softmax_probs / softmax_probs.sum())

        # Return the recommended products
        return [category_products[i] for i in recommended_indices]
