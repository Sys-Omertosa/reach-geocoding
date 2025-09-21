import requests
from bs4 import BeautifulSoup
import os
import time
import csv

# Scraper to bulk collect NDMA-NEOC projections 

BASE_URL = "https://www.ndma.gov.pk/projection-impact-list_new"
OUTPUT_FILE = "ndma_neoc_projections_bulk.csv"

###############################################
# Extract all required fields from a single entry
def process_entry(div):
    # Title
    title_tag = div.find("h5", class_="proj-title")
    title = title_tag.get_text(strip=True) if title_tag else None

    # Date
    date_tag = div.find("span", class_="proj-date")
    date = date_tag.get_text(strip=True) if date_tag else None

    # URL - capture all file types
    a_tag = div.find("a", href=True)
    url = None
    filename = None
    file_type = None
    
    if a_tag and a_tag.get("href"):
        href = a_tag["href"]
        url = href
        filename = os.path.basename(url)
        
        # Determine file type from extension
        if filename and '.' in filename:
            file_type = filename.split('.')[-1].lower()
        else:
            file_type = "unknown"

    return {
        "date": date,
        "source_agency": "NDMA-NEOC",
        "title": title,
        "source_page": BASE_URL,
        "filename": filename,
        "url": url,
        "file_type": file_type
    }

###############################################
# Extract the projection divs from a single page
def process_page(page_number):
    # Parse html
    page_url = BASE_URL + f"?page={page_number}"
    
    try:
        response = requests.get(page_url, timeout=30)
        response.raise_for_status()  # Fixed: added missing parentheses
    except requests.RequestException as e:
        print(f"Error fetching page {page_number}: {e}")
        return []

    parsed_page = BeautifulSoup(response.content, "html.parser")

    # Find all projection divs - capture ALL entries, not just PDFs
    divs = parsed_page.find_all("div", class_="panel panel-default proj-card")
    
    return divs

###############################################
# Bulk scrape by iterating through all pages
def process_bulk():
    all_data = []
    page_number = 1
    print(f"Bulk scraping projections from {BASE_URL}")

    # Loop through pages
    while True:
        divs = process_page(page_number)
        if not divs:
            print("No more entries found. Exiting scraping.")
            break
            
        print(f"Scraped page number {page_number}, found {len(divs)} entries")
        
        # Process each div to extract structured data
        for div in divs:
            entry_data = process_entry(div)
            # Add all entries, even those without URLs (for debugging/completeness)
            all_data.append(entry_data)
        
        page_number += 1
        time.sleep(10)  # Be respectful to the server

    return all_data

###############################################
# Dump all to CSV
def dump_csv(data):
    # Give integer IDs
    for i, entry in enumerate(data, start=1):
        entry["id"] = i
    
    fieldnames = ["id", "date", "source_agency", "title", "source_page", "filename", "url", "file_type"]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

    print(f"Saved {len(data)} advisories from NDMA-NEOC to {OUTPUT_FILE}")

if __name__ == "__main__":
    advisories = process_bulk()
    dump_csv(advisories)