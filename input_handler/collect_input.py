# input_handler/collect_input.py

import json
import os

def collect_input():
    print("\n📝 Enter product and target details:\n")
    
    product_name = input("Product Name: ").strip()
    product_description = input("Product Description: ").strip()
    target_consumer = input("Target Consumer (e.g., marketing teams in e-commerce companies): ").strip()
    company_type = input("Type of Target Companies (e.g., startups, large enterprises): ").strip()
    location = input("Preferred Company Location (e.g., India, US, Europe, or global): ").strip()

    data = {
        "product_name": product_name,
        "product_description": product_description,
        "target_consumer": target_consumer,
        "company_type": company_type,
        "location": location
    }

    # Save to root-level data/input.json
    root_data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(root_data_path, exist_ok=True)
    input_path = os.path.join(root_data_path, "input.json")

    with open(input_path, "w") as f:
        json.dump(data, f, indent=2)

    print("\n✅ Input saved to data/input.json")

if __name__ == "__main__":
    collect_input()
