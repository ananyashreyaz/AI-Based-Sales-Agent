import json
import os

def collect_input():
    print("📩 SALES AGENT: INPUT HANDLER\n")

    product_name = input("Enter your product name: ")
    product_description = input("Describe your product briefly: ")
    target_consumer = input("Who is your target consumer? (industry/role): ")

    input_data = {
        "product_name": product_name.strip(),
        "product_description": product_description.strip(),
        "target_consumer": target_consumer.strip()
    }

    os.makedirs("data", exist_ok=True)
    with open("data/product_input.json", "w") as f:
        json.dump(input_data, f, indent=4)

    print("\n✅ Input saved to data/product_input.json")

if __name__ == "__main__":
    collect_input()
