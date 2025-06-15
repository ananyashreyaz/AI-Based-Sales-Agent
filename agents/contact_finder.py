import os
import csv
import json
import time
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR-API-KEY")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

INPUT_FILE = os.path.join("..", "data", "company_list.csv")
OUTPUT_FILE = os.path.join("..", "data", "company_list.csv")

def build_prompt(company_name, website, department):
    return f"""
You are a B2B contact research assistant.

For the given company, find decision-makers according to the following rules:

Company Name: {company_name}  
Company Website: {website}  
Relevant Department: {department}  

Rules:
1. First, try to find the Head of the specified department (e.g., "Head of Marketing", "VP of Engineering").
2. If no one from that department is found, provide the founder or CEO's details instead.
3. Return only 1 most relevant person.

Include the following details:
- Full Name
- Designation / Job Title
- Verified Email Address
- LinkedIn Profile URL (if available)
- Work Phone Number (if available)

Format your output as JSON like this:
```json
{{
  "name": "John Doe",
  "title": "Head of Marketing",
  "email": "john.doe@company.com",
  "linkedin": "https://linkedin.com/in/johndoe",
  "phone": "+91-9876543210"
}}
```

Only return valid and real-world information. Do not hallucinate. If no contact is found at all, return:
```json
{{ "error": "No contact available" }}
```
"""

def load_company_list():
    with open(INPUT_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def append_contact_result(company_name, website, department, contact):
    file_exists = os.path.isfile(OUTPUT_FILE)
    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["company_name", "website", "department", "name", "title", "email", "linkedin", "phone"])
        writer.writerow([
            company_name,
            website,
            department,
            contact.get("name", ""),
            contact.get("title", ""),
            contact.get("email", ""),
            contact.get("linkedin", ""),
            contact.get("phone", "")
        ])

def find_contact(company_name, website, department):
    prompt = build_prompt(company_name, website, department)
    try:
        response = model.generate_content(prompt)
        contact_json = json.loads(response.text.strip().split("```json")[1].split("```")[0])
        return contact_json
    except Exception as e:
        print(f"[❌] Error fetching contact for {company_name}: {e}")
        return {"error": "Parsing/Generation Failed"}

def main():
    print("🤖 Running Contact Finder Agent...")
    companies = load_company_list()

    for company in companies:
        name = company.get("company_name", "").strip()
        website = company.get("website", "").strip()
        dept = company.get("department", "").strip()

        if not name or not website:
            print(f"⚠️ Skipping incomplete record: {company}")
            continue

        print(f"🔍 Searching contact for: {name}")
        contact = find_contact(name, website, dept)

        if "error" in contact:
            print(f"⚠️ No contact found for {name}")
        else:
            append_contact_result(name, website, dept, contact)
            print(f"✅ Contact saved for {name}")

        time.sleep(1)  # Respectful delay

    print(f"\n📁 All contacts saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
