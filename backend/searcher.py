from collections import defaultdict
import math
from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity




def calculate_tfxidf(inverted_index, size):
    # inverted_index: a dictionary. key: term, value: list of tuples (page id, term frequency)
    
    # df: a dictionary. key: term, value: df, number of documents that contain the term
    df = defaultdict(int)
    for term, doc_freq in inverted_index.items():
        df[term] = len(doc_freq)

    # idf: a dictionary. key: term, value: idf value of the term
    idf = {term: math.log2(size/df[term]) for term in df}

    max_tf = 0
    for doc_freq in inverted_index.values():
        if(max_tf < doc_freq[1]): max_tf = doc_freq[1]

    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf_weight}
    # tf-idf weight is calculated by: tfxidf/max(tf) 
    tf_idf_weights = {}
    for term, doc_freq in inverted_index.items():
        for doc_id, tf in doc_freq:
            tf_idf_weights.setdefault(term, {}).update({doc_id: (1 + math.log2(tf)) * idf[term]}/max_tf)

    return tf_idf_weights




def calculate_similarity(query, keyword_weights, title_weights, FAVOR):
    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf_weight}

    all_terms = set(keyword_weights.keys()).union(set(title_weights.keys())).union(set(query))
    
    query_vector = {term: 0 for term in all_terms}
    for term in query:
        query_vector[term] = 1
    
    doc_vectors = []
    for doc_id in keyword_weights.keys():
        doc_vectors[doc_id] = {term: 0 for term in all_terms}
        for term in all_terms:
            if term in keyword_weights.keys():
                doc_vectors[doc_id][term] += keyword_weights[term][doc_id]
            if term in title_weights.keys():
                doc_vectors[doc_id][term] += title_weights[term][doc_id] * FAVOR
            if term not in keyword_weights.keys() and term not in title_weights.keys():
                doc_vectors[doc_id][term] = 0
        
    
    docs_similarity = []
    for doc_id in range(len(doc_vectors)):
        score = cosine_similarity(query_vector, doc_vectors[doc_id])
        docs_similarity[doc_id] = score
        
    return docs_similarity




def retrieval_function(query, keyword_index, title_index, max_pages):
    # A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
    # up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
    #     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
    #     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page
    
    FAVOR = 1.5 # a constant to boost the rank of a page if there is a match in the title


    # the weights are nested dictionary containing weights
    # outer dictionary - key: term  value: inner dictionary
    # inner dictionary - key: doc_id value: tfxidf weight
    keyword_weights = calculate_tfxidf(keyword_index, max_pages)
    title_weights = calculate_tfxidf(title_index, max_pages)

    # docs_similarity: a list - index: doc_id, value: cosine similarity
    docs_similarity = calculate_similarity(query, keyword_weights, title_weights, FAVOR)


    top_doc = 0 # page_id of the top document

    for doc_id in range(len(docs_similarity)): 
        if docs_similarity[doc_id] > docs_similarity[top_doc]: 
            top_doc = doc_id 


    return top_doc