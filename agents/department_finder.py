import os
import csv
import json
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyCfelKcj2UIieWpF9yMQny_dNqKprWS4vc")
genai.configure(api_key=GEMINI_API_KEY)

INPUT_FILE = os.path.join("..", "data", "company_list.csv")
INPUT_JSON = os.path.join("..", "data", "input.json")


def load_input_details():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("product_description", "")


def load_companies():
    companies = []
    with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            companies.append({
                "company_name": row.get("company_name", "") or row.get("name", ""),
                "company_website": row.get("company_website", "") or row.get("website", "")
            })
    return companies


def build_prompt(company, product_description):
    return f'''
You are an AI assistant helping identify the most relevant department in a company that would be interested in a B2B SaaS product.

Product Description: {product_description}

Company Name: {company['company_name']}
Company Website: {company['company_website']}

List only the most relevant department that would be interested in this product. Also check if that department exists in that company or not. If no such department is obvious, return "Marketing".
Do not explain anything. Just return the department name.
'''


def find_departments(companies, product_description):
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    results = []

    for company in companies:
        print(f"🔍 Finding department for: {company['company_name']}")
        try:
            prompt = build_prompt(company, product_description)
            response = model.generate_content(prompt)
            department = response.text.strip().split("\n")[0].strip("•- ").strip()
            results.append({
                "company_name": company["company_name"],
                "company_website": company["company_website"],
                "department": department
            })
        except Exception as e:
            print(f"[❌] Error for {company['company_name']}: {e}")
            results.append({
                "company_name": company["company_name"],
                "company_website": company["company_website"],
                "department": ""
            })

    return results


def update_csv(companies_with_departments):
    fieldnames = ["company_name", "company_website", "department"]
    with open(INPUT_FILE, "w", newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for company in companies_with_departments:
            filtered_row = {key: company.get(key, "") for key in fieldnames}
            writer.writerow(filtered_row)


def main():
    print("🤖 Running Department Finder Agent...")
    product_description = load_input_details()
    companies = load_companies()
    enriched = find_departments(companies, product_description)
    update_csv(enriched)
    print(f"✅ Updated {len(enriched)} companies with department info.")


if __name__ == "__main__":
    main()
