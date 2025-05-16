import requests
import pandas as pd
import time

# Constants
API_BASE_URL = "https://api.reporter.nih.gov/v2/projects/search"
FISCAL_YEAR = 2025
REQUEST_LIMIT = 500  # NIH API max limit per request
OUTPUT_FILENAME_BASE = "nih_grants_2025"


def fetch_all_grants(fiscal_year):
    """
    Fetch up to REQUEST_LIMIT grant records for the specified fiscal year from the NIH RePORTER API.
    Returns a list of grant records (dictionaries).
    """
    payload = {
        "criteria": {
            "fiscal_years": [fiscal_year]
        },
        "limit": REQUEST_LIMIT
        # No 'include_fields' to get all fields
    }
    response = requests.post(API_BASE_URL, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])


def export_data(df, format_choice):
    """
    Export the DataFrame to the specified format (csv or xlsx).
    Returns the filename used for export.
    """
    if format_choice.lower() == 'csv':
        filename = f"{OUTPUT_FILENAME_BASE}.csv"
        df.to_csv(filename, index=False)
    else:  # xlsx
        filename = f"{OUTPUT_FILENAME_BASE}.xlsx"
        df.to_excel(filename, index=False)
    return filename


def get_export_format():
    """
    Get the desired export format from user input.
    Returns either 'csv' or 'xlsx'.
    """
    while True:
        choice = input("Choose export format (csv/xlsx): ").lower().strip()
        if choice in ['csv', 'xlsx']:
            return choice
        print("Invalid choice. Please enter either 'csv' or 'xlsx'.")


def main():
    # Fetch all grants for the specified fiscal year (up to cap)
    all_grants = fetch_all_grants(FISCAL_YEAR)
    if not all_grants:
        print("No grant data found.")
        return

    # Convert to DataFrame
    df = pd.DataFrame(all_grants)
    
    # Get export format choice from user
    format_choice = get_export_format()
    
    # Export data in chosen format
    output_file = export_data(df, format_choice)
    print(f"Exported {len(df)} grants to {output_file}")


if __name__ == "__main__":
    main() 