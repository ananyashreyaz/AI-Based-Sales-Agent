# agents/company_finder.py

import os
import json
import csv
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
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
        "List 10 real companies in that location that would benefit from this product. "
        "Return the result as a JSON list with this format:\n"
        "[\n"
        "  {\"company_name\": \"Company A\", \"company_website\": \"https://www.companya.com\"},\n"
        "  ...\n"
        "]\n"
        "Pay attention on target company type and according to that find the names of the companies Also the links should be working, official websites of those companies. Do not include explanations or extra formatting."
    )

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(prompt)

    try:
        start = response.text.find("[")
        end = response.text.rfind("]") + 1
        json_text = response.text[start:end]
        company_data = json.loads(json_text)
        return company_data
    except Exception as e:
        print("❌ Error parsing Gemini output:", e)
        print("Raw response:\n", response.text)
        return []

def save_companies(companies):
    os.makedirs("data", exist_ok=True)
    csv_path = os.path.join("..", "data", "company_list.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["company_name", "company_website"])
        writer.writeheader()
        for company in companies:
            writer.writerow(company)

    print(f"\n✅ Saved {len(companies)} companies to {csv_path}")

def main():
    print("🤖 Running Company Finder Agent...")
    input_data = load_input()
    companies = generate_company_list(input_data)

    if not companies:
        print("⚠️ No companies returned by Gemini.")
        return

    print("🏢 Companies found:")
    for c in companies:
        print(f"- {c['company_name']} ({c['company_website']})")

    save_companies(companies)

if __name__ == "__main__":
    main()
