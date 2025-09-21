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
    title_tag = div.find("h5", class_ = "proj-title")
    title = title_tag.get_text(strip = True) if title_tag else None

    #Date
    date_tag = div.find("span", class_ = "proj_date")
    date = date_tag.get_text(strip = True) if date_tag else None

    #URL
    a_tag = div.find("a", href = True)
    url = a_tag["href"] if a_tag["href"].lower().endswith(".pdf") else None

    #Filename
    filename = os.path.basename(url)

    return {
        "date": date,
        "source_agency": "NDMA-NEOC",
        "title": title,
        "source_page": BASE_URL,
        "filename": filename,
        "url": url
    }

###############################################
# Extract the projection divs from a single page
def process_page(page_number):

    #Parse html
    page_url = BASE_URL + f"?page={page_number}"
    response = requests.get(page_url)
    response.raise_for_status
    parsed_page = BeautifulSoup(response.content, "html.parser")

    #Find projection divs, containing ahref with pdf
    projections = []
    for div in parsed_page.find_all("div", class_="panel panel-default proj-card"):
        if div.find("a", href = True)["href"].lower().endswith(".pdf"):
            projections.append(div)

    return projections

###############################################
# Bulk scrape by interating through all pages
def process_bulk():

    all_data = []
    page_number = 1
    print(f"Bulk scraping projections from {BASE_URL}")

    # Loop through pages
    while True:
        entries = process_page(page_number)
        if not entries:
            print("No more entries found. Exiting scraping.")
            break
        print(f"Scraped page number {page_number}")
        page_number += 1

        # Attach collected formatted data to list
        all_data.extend(entries)
        time.sleep(10)

    return all_data

###############################################
# Dump all to CSV
def dump_csv(data):
    
    # Give integer IDs
    for i, entry in enumerate(data, start=1):
        entry["id"] = i
    
    fieldnames = ["id", "date", "source_agency",  "title", "source_page", "filename", "url"]

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

        print(f"Saved {len(data)} advisories from NDMA-NEOC to {OUTPUT_FILE}")


if __name__ == "__main__":
    advisories = process_bulk()
    dump_csv(advisories)