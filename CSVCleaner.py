import pandas as pd
import re
import os
from glob import glob

def extract_phone(text):
    m = re.search(r'(?:Phone[: ]*\s*)([\d\-\.\(\) ]{6,})', str(text), re.IGNORECASE)
    return m.group(1).strip() if m else ""

def extract_fax(text):
    m = re.search(r'(?:Fax[: ]*\s*)([\d\-\.\(\) ]{6,})', str(text), re.IGNORECASE)
    return m.group(1).strip() if m else ""

def extract_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', str(text))
    return m.group(0) if m else ""

def extract_website(text):
    m = re.search(r'(https?://[^\s,;]+)', str(text))
    return m.group(1).strip() if m else ""

def split_address(addr):
    if pd.isna(addr) or str(addr).strip() == "":
        return ["", "", "", "", "", ""]

    # Normalize weird spaces and html entities
    addr = str(addr).replace("\u00a0", " ").replace("&#8211;", "-").strip()

    # Basic Canadian postal code extraction (A1A 1A1)
    postal = ""
    m = re.search(r'([A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d)', addr)
    if m:
        postal = m.group(1)
    # Split on commas or newlines
    parts = re.split(r'[,\n]+', addr)
    parts = [p.strip() for p in parts if p.strip()]
    address1 = parts[0] if len(parts) > 0 else ""
    address2 = parts[1] if len(parts) > 2 else ""
    city = ""
    province = ""
    country = "Canada"
    # Heuristic: try to find province abbreviation in the last part
    if len(parts) >= 1:
        last = parts[-1]
        prov_match = re.search(r'\b(AB|BC|SK|MB|ON|QC|NB|NS|NL|PE|YT|NT|NU)\b', last, re.IGNORECASE)
        if prov_match:
            province = prov_match.group(1).upper()
            # try to get city from the part before last
            if len(parts) >= 2:
                city = parts[-2]
        else:
            if len(parts) >= 3:
                city = parts[-2]
                province = parts[-1]

    return [address1, address2, city, province, postal, country]

INPUT_DIR = ""      # change to your folder path
OUTPUT_FILE = ""      # change this to set your filename and directory

all_files = glob(os.path.join(INPUT_DIR, "*.csv"))

if not all_files:
    print("No CSV files found in directory:", INPUT_DIR)
    raise SystemExit(1)

merged_records = []

for file in all_files:
    filename = os.path.basename(file)

    # Normalize filename entity and whitespace
    # Remove extension first
    name_no_ext = re.sub(r'\.csv$', '', filename, flags=re.IGNORECASE)

    # Pattern: remove leading "Directory" (case-insensitive) and any dash variants that follow,
    # including the HTML entity &#8211;
    # Examples handled:
    #   "Directory &#8211; Accounting and Financial Services"
    #   "Directory - Restaurants and Food Services"
    #   "Directory – Oilfield Services"
    #   "directory—Some Category"
    type_value = re.sub(r'(?i)^\s*directory\s*(?:&#8211;|&ndash;|–|—|-)\s*', '', name_no_ext).strip()
    if not type_value:
        type_value = re.sub(r'(?i)^\s*directory\s*[:\-–—]*\s*', '', name_no_ext).strip()
    if not type_value:
        type_value = name_no_ext.strip()
    print(f"Processing: {filename}  ->  Type: '{type_value}'")
    try:
        df = pd.read_csv(file, dtype=str, encoding='utf-8')
    except Exception:
        df = pd.read_csv(file, dtype=str, encoding='latin-1')
    df.columns = [c.strip() for c in df.columns]
    for _, row in df.iterrows():
        name = row.get("NAME", "") or row.get("Name", "") or ""
        addr = row.get("ADDRESS", "") or row.get("Address", "") or ""
        contact = row.get("CONTACT", "") or row.get("Contact", "") or ""
        services = row.get("SERVICES", "") or row.get("Services", "") or ""
        phone = extract_phone(contact)
        fax = extract_fax(contact)
        email = extract_email(contact)
        website = extract_website(contact)
        address1, address2, city, prov, postal, country = split_address(addr)
        merged_records.append({
            "Type": type_value,
            "Name": name,
            "Phone": phone,
            "Fax": fax,
            "Address 1": address1,
            "Address 2": address2,
            "City/Town": city,
            "Country": country,
            "Province/State": prov,
            "Postal/Zip Code": postal,
            "Website": website,
            "Description": services,
            "Show on Map (Y/N)": "Y",
            "Area": "",
            "Subtitle": "",
            "Latitude": "",   # intentionally left blank
            "Longitude": "",  # intentionally left blank
            "Email": email
        })
out_df = pd.DataFrame(merged_records, columns=[
    "Type", "Name", "Phone", "Fax", "Address 1", "Address 2", "City/Town", "Country",
    "Province/State", "Postal/Zip Code", "Website", "Description", "Show on Map (Y/N)",
    "Area", "Subtitle", "Latitude", "Longitude", "Email"
])
out_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')

print(f"\nDone — merged {len(all_files)} file(s). Output saved to: {OUTPUT_FILE}")