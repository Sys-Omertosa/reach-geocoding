import requests
from bs4 import BeautifulSoup
import os
import time
import csv

# Scraper for bulk collecting all available NDMA advisories

BASE_URL = "https://www.ndma.gov.pk/advisories"

##################################
# Extract metadata from a single entry
def ndma_advisory_entry(a_tag):

    pdf_url = a_tag["href"]
    filename = os.path.basename(pdf_url)

    # date
    date_tag = a_tag.find("p", class_="advisory-date")
    date_text = date_tag.get_text(strip=True) if date_tag else None

    # title
    title_tag = a_tag.find("h4", class_="advisory-title text-black")
    title_text = title_tag.get_text(strip=True) if title_tag else None

    return {
        "date": date_text,
        "source_agency": "NDMA",
        "title": title_text,
        "source_page": BASE_URL,
        "filename": filename,
        "url": pdf_url
    }

##################################
# Extract all advisory entries on a single page
def ndma_advisory_page(page_number: int):

    # parse html
    page_url = BASE_URL + f"?page={page_number}"
    response = requests.get(page_url)
    response.raise_for_status()
    parsed_page = BeautifulSoup(response.content, "html.parser")

    # find <a> tags
    advisories = []
    for a in parsed_page.find_all("a", href=True):
        if a["href"].lower().endswith(".pdf"):
            advisories.append(ndma_advisory_entry(a))

    return advisories

##################################
# Iterate through all pages
def ndma_advisories_bulk():

    all_data = []
    page_number = 1
    print(f"Bulk scraping {BASE_URL}")

    # Loop through pages
    while True:
        entries = ndma_advisory_page(page_number)
        if not entries:
            print("No more advisories found")
            break
        print(f"Scraped page number {page_number}")
        page_number += 1

        # Attach collected formatted data to list
        all_data.extend(entries)
        time.sleep(10)

    return all_data

##################################
# Dump all to CSV
def save_ndma_csv_bulk(data, filename="ndma_advisories_bulk.csv"):
    
    # Give integer IDs
    for i, entry in enumerate(data, start=1):
        entry["id"] = i
    
    fieldnames = ["id", "date", "source_agency",  "title", "source_page", "filename", "url"]

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

        print(f"Saved {len(data)} advisories from NDMA to {filename}")


if __name__ == "__main__":
    advisories = ndma_advisories_bulk()
    save_ndma_csv_bulk(advisories)