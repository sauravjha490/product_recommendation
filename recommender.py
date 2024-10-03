# recommender.py

import numpy as np
import tensorflow as tf
from data import products, user_preferences

class RecommendationSystem:
    def __init__(self):
        self.products = products
        self.user_preferences = user_preferences
        self.model = self.build_model()
        self.train_model()

    def build_model(self):
        # Simple model to recommend products based on user interactions
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(2,)),  # Input for user and product indices
            tf.keras.layers.Dense(32, activation='relu'),  # Increased hidden layer size
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(len(products), activation='softmax')  # Output layer
        ])
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        return model

    def prepare_data(self):
        user_ids = []
        product_ids = []
        for entry in self.user_preferences:
            user_ids.append(entry['user_id'])
            product_ids.append(entry['purchased_product_id'])
        return np.array(user_ids), np.array(product_ids)

    def train_model(self):
        user_ids, product_ids = self.prepare_data()
        # Fit the model with user-product pairs
        self.model.fit(np.array(list(zip(user_ids, product_ids))), product_ids, epochs=50)  # Increase epochs

    def recommend_by_category(self, category):
        # Generate recommendations for a given category
        category_products = [product for product in self.products if product['category'] == category]
        
        if not category_products:
            return []

        # Prepare input for the model
        product_indices = [p['id'] for p in category_products]
        user_indices = np.zeros(len(product_indices))  # Assuming a dummy user index for demo

        # Make predictions
        predictions = self.model.predict(np.array(list(zip(user_indices, product_indices))))

        # Get the indices of the top 2 products
        recommended_indices = np.argsort(predictions[0])[-2:]  # Get top 2 indices

        # Return the recommended products
        return [category_products[i] for i in recommended_indices if i < len(category_products)]
