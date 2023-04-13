from collections import defaultdict
import math
from scipy.spatial.distance import cosine




def calculate_tfxidf(inverted_index, size):
    # inverted_index: a dictionary. key: term, value: list of tuples (page id, term frequency)
    
    # df: a dictionary. key: term, value: df, number of documents that contain the term
    df = defaultdict(int)
    for term, doc_freq in inverted_index.items():
        df[term] = len(doc_freq)

    # idf: a dictionary. key: term, value: idf value of the term
    idf = {term: math.log2(size/df[term]) for term in df}


    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf weight}
    tf_idf_weights = {}
    for term, doc_freq in inverted_index.items():
        for doc_id, tf in doc_freq:
            tf_idf_weights.setdefault(term, {})[doc_id] = (1 + math.log2(tf)) * idf[term]

    return tf_idf_weights



def calculate_similarity(query, keyword_weights, title_weights, FAVOR):
    # weights: a dictionary. key: term, value: dictionary,  {doc_id: (tf-idf weight, term frequency)}

    similarity = {} # default dict is not hashable! so we use another way to initialize here
    for doc in keyword_weights.values():
        for doc_id in doc.keys():
            similarity[doc_id] = 0 # dict isn't hashable

    
    query_vector = []
    for word in query:
        keyword_weight = 0
        title_weight = 0
        if word in keyword_weights.keys():
            keyword_weight = keyword_weights[word]
        # if word in title_weights.keys():
        #     title_weight = FAVOR * title_weights[word]
        for word, weights in title_weights.items():
            for doc_id, weight in weights.items():
                keyword_weight
                
        combined_weight = {doc_id: (keyword_weight.get(doc_id, 0)[0] + title_weight.get(doc_id, 0)[0]) for doc_id in similarity.keys()} # get(doc_id, 0) means that the default value of doc_id is 0
        query_vector.append(combined_weight)


    # iterate each document and generate a document vector
    for doc_id in similarity.keys():
        doc_vector = []
        for word in query:
            keyword_weight = 0
            title_weight = 0
            if word in keyword_weights.keys():
                keyword_weight = keyword_weights[word].get(doc_id, (0, 0))[0]
            if word in title_weights.keys():
                title_weight = FAVOR * title_weights[word].get(doc_id, (0, 0))[0]
            doc_vector.append(keyword_weight + title_weight)

        similarity[doc_id] = 1 - cosine(list(query_vector[i][doc_id] for i in range(len(query))), doc_vector)


    # simialrity: a dictionary. key: doc_id, value: cosine similarity
    return similarity




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

    similarity = calculate_similarity(query, keyword_weights, title_weights, FAVOR)


    top_doc = 0 # page_id of the top document

    for doc_id in similarity.keys(): 
        if similarity[doc_id] > similarity[top_doc]: 
            top_doc = doc_id 


    return top_doc