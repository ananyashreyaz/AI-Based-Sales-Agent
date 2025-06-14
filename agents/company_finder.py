# agents/company_finder.py

import os
import json
import csv
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR-API-KEY")
genai.configure(api_key=GEMINI_API_KEY)

def load_input():
    with open("../data/input.json") as f:
        return json.load(f)

def generate_company_list(input_data):
    prompt = (
    f"You are a B2B market research assistant.\n\n"
    f"Product: {input_data['product_name']}\n"
    f"Description: {input_data['product_description']}\n"
    f"Target Audience: {input_data['target_consumer']}\n"
    f"Target Company Type: {input_data['company_type']}\n"
    f"Location Preference: {input_data['location']}\n\n"
    "List 10 real companies in that location that would be highly likely to benefit from this product. "
    "Only return the company names as bullet points. Pay special attention to the company type. Do not explain anything else."
)


    model = genai.GenerativeModel("models/gemini-1.5-flash")

    response = model.generate_content(prompt)
    
    lines = response.text.split("\n")
    companies = [line.strip("•- \n") for line in lines if len(line.strip()) > 2]
    return list(set(companies))  # remove duplicates

def save_companies(companies):
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("..", "data", "company_list.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["company_name"])
        for name in companies:
            writer.writerow([name])
    print(f"\n✅ Saved {len(companies)} companies to {csv_path}")

def main():
    print("🤖 Running Company Finder Agent...")
    input_data = load_input()
    companies = generate_company_list(input_data)

    if not companies:
        print("⚠️ No companies returned by Gemini.")
        return

    print(f"🏢 Companies found: {companies}")
    save_companies(companies)

if __name__ == "__main__":
    main()
