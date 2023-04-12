import indexer
import crawler
from collections import defaultdict
import math

def calculate_tfxidf(inverted_index, size):
    # inverted_index: a dictionary. key: term, value: list of tuples (page id, term frequency)

    # df: a dictionary. key: term, value: df, number of documents that contain the term
    df = defaultdict(int)
    for term, doc_freq in inverted_index.items():
        df[term] = len(doc_freq)

    # idf: a dictionary. key: term, value: idf value of the term
    idf = {term: math.log2(size/df[term]) for term in df}

    tf_idf_weights = defaultdict(lambda: defaultdict(float)) 
    # outer dictionary should be initialized with an inner dictionary for each new key
    # inner dictionary should be initialized with a default value of float(0) for each new key
    
    for term, doc_freq in inverted_index.items():
        doc_id = doc_freq[0]
        tf = doc_freq[1]
        tf_idf_weights[term][doc_id] = (1 + math.log2(tf)) * idf[term]

    return tf_idf_weights



def retrieval_function(query, keyword_index, title_index, max_pages):
    # A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
    # up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
    #     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
    #     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page
    
    FAVOR_TITLE = 1.5 # a constant to boost the rank of a page if there is a match in the title

    keyword_weights = calculate_tfxidf(keyword_index, max_pages)
    title_weights = calculate_tfxidf(title_index, max_pages)



    top_doc = 0 # page_id of the top document



    return top_doc