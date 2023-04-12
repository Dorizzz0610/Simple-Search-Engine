import indexer
import crawler
from collections import defaultdict
import math

def calculate_tfxidf(inverted_index, documents):
    # Calculate tfxidf/max(tf) for each term in each document
    # Calculate the document frequencies
    df = defaultdict(int)
    for term, doc_freq in inverted_index.items():
        df[term] = len(doc_freq)

    # Calculate the inverse document frequencies
    N = len(documents)
    idf = {term: math.log10(N/df[term]) for term in df}

    # Calculate the tf-idf weights
    tf_idf_weights = defaultdict(lambda: defaultdict(float))
    for term, doc_freq in inverted_index.items():
        for doc_id, tf in doc_freq.items():
            tf_idf_weights[term][doc_id] = (1 + math.log10(tf)) * idf[term]

    return tf_idf_weights



def retrieval_function(query, keyword_index, title_index):
    # A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
    # up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
    #     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
    #     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page
    pass



