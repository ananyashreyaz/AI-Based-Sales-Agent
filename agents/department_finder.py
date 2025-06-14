import os
import csv
import json
import google.generativeai as genai


GEMINI_API_KEY = "YOUR-API-KEY"  
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("models/gemini-1.5-flash")

def load_input():
    with open(os.path.join("..", "data", "input.json"), "r") as f:
        return json.load(f)

def load_companies():
    with open(os.path.join("..", "data", "company_list.csv"), newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def find_department(company_name, input_data):
    prompt = (
        f"You are a B2B research assistant helping a sales agent.\n"
        f"Product: {input_data['product_name']}\n"
        f"Description: {input_data['product_description']}\n"
        f"Target Audience: {input_data['target_consumer']}\n"
        f"Target Company Type: {input_data['company_type']}\n"
        f"Location: {input_data['location']}\n\n"
        f"For the company '{company_name}', which department should the sales team contact about this product?, also check if that department for  the particular company exists or not.\n"
        f"Respond with only the department name."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"⚠️ Error for {company_name}: {e}")
        return "Unknown"

def save_companies(updated_list):
    path = os.path.join("..", "data", "company_list.csv")
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company_name", "department"])
        writer.writeheader()
        writer.writerows(updated_list)

def main():
    print("Running Department Finder Agent...\n")
    input_data = load_input()
    companies = load_companies()

    updated_companies = []
    for company in companies:
        name = company["company_name"]
        dept = find_department(name, input_data)
        updated_companies.append({"company_name": name, "department": dept})
        print(f"🏢 {name} → 📂 {dept}")

    save_companies(updated_companies)
    print("\n✅ Departments updated and saved to data/company_list.csv")

if __name__ == "__main__":
    main()
