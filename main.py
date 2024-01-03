import pandas as pd
from collections import Counter, defaultdict
from pre_processing import preprocess_content

# Load the inverted index from the saved CSV
inverted_index_df = pd.read_csv('inverted_index_live.csv')

# Convert the DataFrame back to the inverted index format
inverted_index = defaultdict(dict)  # Use a dictionary instead of a list
for _, row in inverted_index_df.iterrows():
    term = row['Term']
    doc_id = row['DocumentID']
    frequency = row['Frequency']
    inverted_index[term][doc_id] = frequency

# Load document links from the saved CSV
document_links_df = pd.read_csv('document_links_live.csv')

# Convert the DataFrame to a dictionary
document_links = {}
for _, row in document_links_df.iterrows():
    doc_id = row['DocumentID']
    link = row['Link']
    heading = row['Heading']
    summary = row['Summary']
    document_links[doc_id] = {'Link': link, 'Heading': heading, 'Summary': summary}

def get_first_two_lines(text):
    # Extract the first two lines from the text
    lines = text.split('.')
    return '\n'.join(lines[:2])

def search(query, inverted_index, document_links):
    # Preprocess the user query
    preprocessed_query = preprocess_content(query)

    # Tokenize the query
    query_terms = preprocessed_query.split()

    # Retrieve lists of documents for each term in the query from the inverted index
    document_lists = [inverted_index[term] for term in query_terms if term in inverted_index]

    # Combine and rank documents based on relevance score
    relevance_scores = Counter()
    for document_list in document_lists:
        for doc_id, frequency in document_list.items():
            relevance_scores[doc_id] += frequency

    # Calculate the total count of relevant documents for the current query
    total_relevant_documents = len(set(relevance_scores))

    # Rank documents based on relevance score
    ranked_documents = relevance_scores.most_common(100)

    # Collect search results in a list
    search_results = []
    for doc_id, relevance_score in ranked_documents:
        document_info = document_links.get(doc_id, {"Link": "Link not available", "Heading": "Heading not available",
                                                    "Summary": "Summary not available"})
        summary_preview = get_first_two_lines(document_info['Summary'])
        search_results.append({
            "DocumentID": doc_id,
            "RelevanceScore": relevance_score,
            "Link": document_info['Link'],
            "Heading": document_info['Heading'],
            "Summary": summary_preview
        })

    return search_results, total_relevant_documents




    # print(f"Document Lists: {document_lists}")
    # print(f"Relevance Scores: {relevance_scores}")

    # Calculate the total count of relevant documents for the current query

