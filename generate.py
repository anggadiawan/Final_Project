import os
import pybliometrics
pybliometrics.scopus.init()
from pybliometrics.scopus import ScopusSearch, AbstractRetrieval
import pandas as pd
from datetime import datetime
import traceback
from tqdm import tqdm


# Journals and ISSNs
journals_issns = {
    "Structures": "2352-0124",
    "Engineering Structures": "1873-7323",
    "Building and Environment": "0360-1323",
}

# Year range
start_year = 2000
end_year = datetime.now().year

def fetch_journal_data(issn, start_year, end_year):
    data = []  # List to store results
    for year in range(start_year, end_year + 1): # Loop through each year in the range
        print(f"Fetching data for ISSN: {issn} Year: {year}")

        try:
            # Perform the Scopus search for the specific ISSN and year
            query = f'ISSN("{issn}") AND PUBYEAR = {year}'# Create a query string for the specific year
            search_query = ScopusSearch(query, subscriber=False, download=True) # Perform the search
            print(f"Year: {year}, Results found: {len(search_query.results)}") # Print the number of results

            # Process results
            for doc in tqdm(search_query.results):
                doc_dict = doc._asdict()
                data.append(doc_dict)

        except Exception as e:
            print(f"Error fetching data for ISSN {issn} in {year}: {e}")
            traceback.print_exc()

    return data

# Main process to fetch data and save to CSVs
if __name__ == "__main__":
    for journal, issn in journals_issns.items():
        print(f"Processing journal: {journal} (ISSN: {issn})")
        journal_data = fetch_journal_data(issn, start_year, end_year)

        if journal_data:
            # Save the fetched data to a CSV file
            df = pd.DataFrame(journal_data)
            output_file = f"{journal.replace(' ', '_')}_data.csv"
            df.to_csv(output_file, index=False)
            print(f"Data for {journal} saved to {output_file}.")
        else:
            print(f"No data fetched for {journal}.")
