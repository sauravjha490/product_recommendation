# gui.py

import tkinter as tk
from tkinter import messagebox
from recommender import RecommendationSystem
from data import products

class ProductRecommendationApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Product Recommendation System")

        self.recommender = RecommendationSystem()

        self.product_buttons = {}
        for product in products:
            button = tk.Button(master, text=product['name'], command=lambda p=product: self.get_recommendations(p))
            button.pack(pady=5)
            self.product_buttons[product['id']] = button

    def get_recommendations(self, product):
        category = product['category']
        recommendations = self.recommender.recommend_by_category(category)
        
        if recommendations:
            recommended_products = "\n".join([f"{prod['name']} ({prod['category']})" for prod in recommendations])
            messagebox.showinfo("Recommendations", f"Recommended products in '{category}':\n{recommended_products}")
        else:
            messagebox.showinfo("Recommendations", f"No recommendations available for '{category}'.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductRecommendationApp(root)
    root.mainloop()
