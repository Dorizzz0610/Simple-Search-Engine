from collections import defaultdict
import math
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import indexer

# A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
# up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
#     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
#     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page


def calculate_tfxidf(inverted_index, size):
    # inverted_index: a dictionary. key: term, value: list of tuples (page id, term frequency)
    # df: a dictionary. key: term, value: df, number of documents that contain the term
    df = defaultdict(int)
    for term, doc_tuple_list in inverted_index.items():
        df[term] = 0
        for doc_tuple in doc_tuple_list:
            if(doc_tuple[1] > 0): df[term] += 1

    # idf: a dictionary. key: term, value: idf value of the term
    idf = {term: math.log2(size/df[term]) for term in df}

    # max_tf: a dictionary. key: term, value: max_tf value of the term
    max_tf = {}
    for term, doc_tuple_list in inverted_index.items():
        max_tf[term] = 0
        for doc_tuple in doc_tuple_list:
            if(max_tf[term] < doc_tuple[1]): max_tf[term] = doc_tuple[1]

    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf_weight}
    #    tf-idf weight is calculated by: tfxidf/max(tf) 
    tf_idf_weights = {}
    for term, doc_tuple_list in inverted_index.items():
        for doc_tuple in doc_tuple_list:
            doc_id = doc_tuple[0]
            tf = doc_tuple[1]
            tf_idf_weights[term] = {doc_id: (1 + math.log2(tf)) * idf[term]/max_tf[term]}

    return tf_idf_weights




def calculate_similarity(query, keyword_weights, title_weights, FAVOR, doc_num):
    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf_weight}

    all_terms = set(keyword_weights.keys()).union(set(title_weights.keys())).union(set(query))
    
    query = indexer.stem(query)
    query_vector = {term: 0 for term in all_terms}
    for term in query:
        query_vector[term] = 1
    
    doc_vectors = [{term: 0 for term in all_terms} for i in range(doc_num)]
    for doc_id in range(doc_num):            
        for term in all_terms:
            if term in keyword_weights.keys() and doc_id in keyword_weights[term].keys():
                weight_dict = keyword_weights[term]
                doc_vectors[doc_id][term] += weight_dict[doc_id]
            if term in title_weights.keys() and doc_id in title_weights[term].keys():
                weight_dict = title_weights[term]
                doc_vectors[doc_id][term] += weight_dict[doc_id] * FAVOR

    # Convert query_vector and doc_vectors to matrices
    query_matrix = [list(query_vector.values())]
    doc_matrix = [list(doc_vector.values()) for doc_vector in doc_vectors]

    docs_similarity = []

    for doc_id in range(len(doc_vectors)):
        doc_vector = doc_matrix[doc_id]
        doc_vector = numpy.array(doc_vector).reshape(1, -1)
        score = cosine_similarity(query_matrix, doc_vector)[0]
        docs_similarity.append(score)
        
 
    return docs_similarity




def retrieval_function(query, keyword_index, title_index, max_pages, FAVOR=1.5):
    # FAVOR: a constant to boost the rank of a page if there is a match in the title

    # the weights are nested dictionary containing weights
    # outer dictionary - key: term  value: inner dictionary
    # inner dictionary - key: doc_id value: tfxidf weight
    keyword_weights = calculate_tfxidf(keyword_index, max_pages)
    title_weights = calculate_tfxidf(title_index, max_pages)

    # docs_similarity: a list - index: doc_id, value: cosine similarity
    docs_similarity = calculate_similarity(query, keyword_weights, title_weights, FAVOR, max_pages)
    for doc_id in range(len(docs_similarity)):
        print("doc_id: ", doc_id, "score: ", docs_similarity[doc_id])
    top_doc = docs_similarity.index(max(docs_similarity))
    
    return top_doc