# gui.py

import tkinter as tk
from tkinter import messagebox
from recommender import RecommendationSystem

class ProductRecommendationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Product Recommendation System")
        self.master.geometry("400x400")  # Set a fixed window size
        self.master.configure(bg="#f0f0f0")  # Set background color

        # Initialize the recommender system
        self.recommender = RecommendationSystem()

        # Create a set of unique product categories
        self.categories = set(product['category'] for product in self.recommender.products)

        # Create a title label
        self.title_label = tk.Label(
            self.master,
            text="Welcome to the Product Recommendation System",
            font=("Helvetica", 16, "bold"),
            bg="#f0f0f0",
            padx=10,
            pady=10
        )
        self.title_label.pack()

        # Create product buttons
        self.create_product_buttons()

    def create_product_buttons(self):
        # Create a frame for the buttons to keep them organized
        button_frame = tk.Frame(self.master, bg="#f0f0f0")
        button_frame.pack(pady=10)

        for product in self.recommender.products:
            button = tk.Button(
                button_frame,
                text=product['name'],
                command=lambda category=product['category']: self.show_recommendations(category),
                width=20,  # Set button width for uniformity
                bg="#4CAF50",  # Green background
                fg="white",    # White text
                font=("Helvetica", 12),
                activebackground="#45a049"  # Change color on hover
            )
            button.pack(pady=5)

    def show_recommendations(self, category):
        recommendations = self.recommender.recommend_by_category(category, temperature=1.5, num_recommendations=3)
        if recommendations:
            rec_text = "Recommendations for category '{}':\n\n".format(category)
            rec_text += "\n".join(product['name'] for product in recommendations)
            messagebox.showinfo("Recommendations", rec_text)
        else:
            messagebox.showinfo("Recommendations", "No recommendations available.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductRecommendationApp(root)
    root.mainloop()
