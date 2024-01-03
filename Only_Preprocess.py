import csv
import glob
import os
import time
import nltk
import requests
from collections import Counter, defaultdict
import pandas as pd

from pre_processing import preprocess_content  # Assuming you have a pre_processing module

# Download NLTK resources (if not already downloaded)
nltk.download('stopwords')
nltk.download('punkt')

def get_content_from_link(url):
    try:
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Error during request: {e}")
        return None

def index_documents(documents, doc_id, inverted_index, inverted_index_csv='inverted_index_live.csv'):
    # Initialize term frequencies for the current document
    term_frequencies = Counter()

    # Iterate over preprocessed documents
    for doc in documents:
        # Update term frequencies
        term_frequencies.update(doc.split())

    # Update the inverted index with term frequencies and document references
    for term, frequency in term_frequencies.items():
        inverted_index[term].append({doc_id: frequency})

    # Save the updated inverted index to the CSV file
    save_inverted_index({term: {'doc_id': doc_id, 'frequency': frequency} for term, frequency in term_frequencies.items()}, inverted_index_csv)

def preprocess_and_index_document(doc_id, link, inverted_index, heading, summary, document_links_csv='document_links_live.csv'):
    if doc_id in document_links:
        print(f"Document with ID {doc_id} and link {link} is already preprocessed. Skipping...\n")
        return

    # Fetch content for the link
    content = get_content_from_link(link)

    # Check if content is retrieved successfully before preprocessing
    if content is not None:
        # Preprocess the content
        preprocessed_content = preprocess_content(content)

        # Index the document with heading, summary, and content
        index_documents([preprocessed_content], doc_id, inverted_index)

        # Append the link, heading, summary, and content to the CSV file with their actual content
        append_to_csv({doc_id: {'Link': link, 'Heading': heading, 'Summary': summary, }}, document_links_csv)
    else:
        # Handle the case where content retrieval failed
        print(f"Content retrieval failed for {link}. Skipping...\n")



def append_to_csv(data, csv_file_path='document_links_live.csv'):
    # Convert the data dictionary to a list of tuples
    rows = [(doc_id, data[doc_id]['Link'], data[doc_id]['Heading'], data[doc_id]['Summary']) for doc_id in data]

    # Print the values before appending to the CSV file
    # print("Values of 'rows' before appending:")
    # print(rows)
    # print("\nValues of 'data' dictionary before appending:")
    # print(data)

    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        # Load the existing DataFrame from the CSV file
        existing_df = pd.read_csv(csv_file_path)

        # Append the new data to the existing DataFrame
        new_data_df = pd.DataFrame(rows, columns=['DocumentID', 'Link', 'Heading', 'Summary'])
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)

        # Drop duplicate rows based on 'DocumentID'
        updated_df.drop_duplicates(subset=['DocumentID'], keep='last', inplace=True)

        # Save the updated DataFrame to the CSV file
        updated_df.to_csv(csv_file_path, index=False)
    else:
        # Save the document links DataFrame to a new CSV file
        document_links_df = pd.DataFrame(rows, columns=['DocumentID', 'Link', 'Heading', 'Summary'])
        document_links_df.to_csv(csv_file_path, index=False)

def save_inverted_index(data, csv_file_path='inverted_index.csv'):
    # Convert the data to a DataFrame for easy storage and retrieval
    rows = []
    for term, info in data.items():
        rows.append([term, info['doc_id'], info['frequency']])

    # Check if the CSV file already exists
    if os.path.exists(csv_file_path):
        # Load the existing DataFrame from the CSV file
        existing_df = pd.read_csv(csv_file_path)

        # Append the new data to the existing DataFrame
        new_data_df = pd.DataFrame(rows, columns=['Term', 'DocumentID', 'Frequency'])
        updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)

        # Drop duplicate rows based on 'Term' and 'DocumentID'
        updated_df.drop_duplicates(subset=['Term', 'DocumentID'], keep='last', inplace=True)

        # Save the updated DataFrame to the CSV file
        updated_df.to_csv(csv_file_path, index=False)
    else:
        # Save the data DataFrame to a new CSV file
        data_df = pd.DataFrame(rows, columns=['Term', 'DocumentID', 'Frequency'])
        data_df.to_csv(csv_file_path, index=False)

def save_document_links(document_links, csv_file_path='document_links.csv'):
    # Convert the document_links dictionary to a DataFrame
    rows = [(doc_id, link, heading, summary) for doc_id, (link, heading, summary) in document_links.items()]
    document_links_df = pd.DataFrame(rows, columns=['DocumentID', 'Link', 'Heading', 'Summary'])

    # Save the document links DataFrame to a CSV file
    document_links_df.to_csv(csv_file_path, index=False)

# Initialize inverted index and document_links
inverted_index = defaultdict(list)
document_links = {}

# Specify the path to your folder containing CSV files
folder_path = r"C:\Users\PMYLS\Downloads\Dawn"

# Get a list of CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Iterate over CSV files
for csv_file_path in csv_files:
    with open(csv_file_path, 'r', encoding='utf-8') as csv_file:
        # Parse CSV content
        csv_reader = csv.reader(csv_file)

        # Skip the first row with column names
        next(csv_reader)

        # Assuming the fourth column contains links
        for idx, row in enumerate(csv_reader, start=1):
            # Check if the row has at least 5 columns (assuming the indices 3, 1, and 4 for link, heading, and summary)
            if len(row) >= 5:
                link_from_csv = row[3]  # Assuming the index is 3 (0-based index)
                heading_from_csv = row[1]  # index for heading
                summary_from_csv = row[4]  # index for summary
                # print(summary_from_csv);
                # print(heading_from_csv);
                # print(link_from_csv);
                # Print a message indicating content is being fetched
                print(f"Fetching content from {link_from_csv}")

                # Process and index the document
                doc_id = f"doc{idx}"
                preprocess_and_index_document(doc_id, link_from_csv, inverted_index, heading_from_csv, summary_from_csv)

                # Store the document link with its ID
                document_links[doc_id] = (link_from_csv, heading_from_csv, summary_from_csv)

                # Add a delay between requests (adjust the value as needed)
                time.sleep(1)

            # Save the final document links after processing all documents in the CSV
save_document_links(document_links)
# Save the inverted index
save_inverted_index(inverted_index)
