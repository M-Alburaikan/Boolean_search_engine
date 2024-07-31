import json
import pickle
import time
import os

def create_index(corpus):
    inverted_index = {}

    for doc_id, document in enumerate(corpus):
        terms = set(document.lower().split())  
        for term in terms:
            inverted_index.setdefault(term, set()).add(doc_id)
    return inverted_index

def boolean_search(query, index):
    or_terms = query.lower().split()  
    result_docs = set()

    for term in or_terms:
        if '&' in term:
            and_terms = term.split('&')
            and_result_docs = set(index.get(and_terms[0], []))
            for t in and_terms[1:]:
                and_result_docs.intersection_update(index.get(t, []))
            result_docs.update(and_result_docs)
        else:
            result_docs.update(index.get(term, []))

    
    #top_results = sorted(result_docs)
    headlines = [news_data[doc_id]['headline'] for doc_id in result_docs]
    return headlines

# Function to save the inverted index to a file
def save_index(index, filename):
    with open(filename, 'wb') as file:
        pickle.dump(index, file)

# Function to load the inverted index from a file
def load_index(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)
    
index_filename = 'inverted_index.pkl'

if os.path.exists(index_filename):
    index = load_index(index_filename)
    print("Inverted index loaded from file.")
    with open('news.json', 'r') as file:
        news_data = [json.loads(line) for line in file]
    
else:
    print("Creating inverted index...")
    with open('news.json', 'r') as file:
        news_data = [json.loads(line) for line in file]
    corpus = [article['short_description'] for article in news_data]
    start_indexing = time.time()
    index = create_index(corpus)
    end_indexing = time.time()
    indexing_time = (end_indexing - start_indexing) * 10**6
    print(f"Inverted index created in {indexing_time:.2f} microseconds.")
    save_index(index, index_filename)
    print("Inverted index created and saved to file.")


queries = [
    "samsung&tv sony&tv lg&tv",
    "is today sunny&day",
    "how to train your dragon",
    "best playstation games coming this year",
    "what is the saudi national anthem",
]

for query in queries:
    start_search = time.time()
    results = boolean_search(query, index)
    end_search = time.time()
    search_time = (end_search - start_search) * 10**6
    print(f"Query: '{query}', Number of results: {len(results)}, Search time: {search_time:.2f} microseconds.\n")
    x=0
    while(x < 10):
        if(x < len(results)):
            print(results[x]+'\n')
        x = x + 1
    print('--------------------------------------------------------')
    