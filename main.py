import requests
from bs4 import BeautifulSoup
import csv
import time

# Base URLs
base_url = "https://www.cmchistn.com/hosp_list_district_multi.php?district="
details_url = "https://www.cmchistn.com/specPopup.php?module=s&id="

# List of districts to scrape
districts = ['ARIYALUR', 'CHENGALPATTU', 'CHENNAI', 'COIMBATORE', 'CUDDALORE', 'DHARMAPURI', 'DINDIGUL', 'ERODE', 'KALLAKURICHI', 'KANCHEEPURAM', 'KANYAKUMARI', 'KARUR', 'KRISHNAGIRI', 'MADURAI', 'MAYILADUTHURAI', 'NAGAPATTINAM', 'NAMAKKAL', 'NILGIRIS', 'PERAMBALUR', 'PUDUKOTTAI', 'RAMANATHAPURAM', 'RANIPET', 'SALEM', 'SIVAGANGAI', 'TENKASI', 'THANJAVUR', 'THENI', 'THIRUPATHUR', 'THIRUVALLUR', 'THIRUVANNAMALAI', 'TIRUCHIRAPPALLI', 'TIRUNELVELI', 'TIRUPPUR', 'TIRUVARUR', 'TUTICORIN', 'VELLORE', 'VILLUPURAM', 'VIRUDHUNAGAR']


output_file = "tamil_nadu_hospitals_detailed.csv"

def get_hospital_details(hospital_id):
    """Fetches detailed information about a hospital using its ID."""
    response = requests.get(details_url + hospital_id)
    response.encoding = response.apparent_encoding  # Detect and use the correct encoding
    soup = BeautifulSoup(response.text, "html.parser")

    details = {}
    rows = soup.select("table tr")
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 2:
            key = cols[0].get_text(strip=True)
            value = cols[1].get_text(strip=True)
            details[key] = value
    return details


def scrape_hospitals_for_district(district):
    """Scrapes hospital list and details for a district."""
    district_hospitals = []
    page = 1

    while True:
        print(f"Scraping page {page} of district {district}...")
        url = f"{base_url}{district}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.select("table tr")
        if not rows or len(rows) == 1:  # No more hospitals
            break

        for row in rows[1:]:  # Skip header row
            cols = row.find_all("td")
            if len(cols) >= 2:
                hospital_id = cols[0].get_text(strip=True)
                hospital_name = cols[1].get_text(strip=True)
                print(f"Fetching details for {hospital_name}...")
                hospital_details = get_hospital_details(hospital_id)
                district_hospitals.append({
                    "District": district,
                    "Hospital ID": hospital_id,
                    "Hospital Name": hospital_name,
                    **hospital_details,
                })
                time.sleep(0.5)  # Avoid overwhelming the server

        # Check if there's a "Next" button for pagination
        if "Next" not in response.text:
            break  # No more pages
        page += 1

    return district_hospitals

def main():
    all_hospitals = []
    for district in districts:
        hospitals = scrape_hospitals_for_district(district)
        all_hospitals.extend(hospitals)

    # Save to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["District", "Hospital ID", "Hospital Name", "ADDRESS", "HOSPITAL CONTACT NO", "AVAILABLE SPECIALITIES"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_hospitals)

    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()