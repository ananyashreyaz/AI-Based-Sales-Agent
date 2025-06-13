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

    # Get absolute path to the project root's data/ folder
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    data_dir = os.path.join(root_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    input_file = os.path.join(data_dir, "product_input.json")
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)

    print(f"\n✅ Input saved to {input_file}")

if __name__ == "__main__":
    collect_input()
