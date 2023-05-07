from collections import defaultdict
import math
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import statistics
import indexer

# A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
# up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
#     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
#     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page


# For single terms
def calculate_tfxidf(inverted_index, size):
    # inverted_index: a dictionary. key: term, value: list of tuples (page id, term frequency)
    # df: a dictionary. key: term, value: df, number of documents that contain the term
    df = defaultdict(int)
    for term, doc_tuple_list in inverted_index.items():
        df[term] = 0
        for doc_tuple in doc_tuple_list:
            if(doc_tuple[1] > 0): df[term] += 1

    # idf: a dictionary. key: term, value: idf value of the term
    idf = {}
    for term in df.keys():
        try:
            idf[term] = math.log2(size/df[term])
        except ZeroDivisionError:
            idf[term] = 0

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
            try:
                tf_idf_weights[term] = {doc_id: (1 + math.log2(tf)) * idf[term]/max_tf[term]}
            except ZeroDivisionError:
                tf_idf_weights[term] = {doc_id: 0}
            except ValueError:
                tf_idf_weights[term] = {doc_id: 0}

    print("tf_idf:", tf_idf_weights)
    return tf_idf_weights



def set_phrases_weight(weights, frequency_dict, max_freq):
    # we set the hardcoded weight of phrase to be a specific percentage of the actual weigths of single terms just calculated
    all_weights = []
    for page_dict in weights.values():
        all_weights.extend(page_dict.values())

    max_weight = max(all_weights)
    median_weight = statistics.median(all_weights)

    base_weight = (max_weight + median_weight) / 3
    print("Phrase base weight:", base_weight)

    phrase_weight = {}
    for doc_id, phrase_freq in frequency_dict.items():
        phrase_weight[doc_id] = {}
        for phrase, freq in phrase_freq.items():
            if(max_freq !=  0): phrase_weight[doc_id][phrase] = base_weight * freq/max_freq
            else: phrase_weight[doc_id][phrase] = 0

    return phrase_weight



def count_phrase(index, query_phrase, doc_num):
    # return the frequency of the phrases in the doc
    phrase_frequency = {}
    max_freq = 0
    for doc_id in range(doc_num):
        phrase_frequency[doc_id] = {}
        for phrase in query_phrase:
            prev_positions = []
            cur_positions = []
            # iterate each word in phrase
            for word in phrase.split():
                if word not in index.keys():
                    # word isn't in any doc body
                    break
                if any(word_page_info[0] == doc_id for word_page_info in index[word]) == False:
                    # word isn't in this doc
                    break

                for word_info in index[word]:
                    if(word_info[0] == doc_id):
                        cur_positions = word_info[2]
                        break
                
                if word == phrase.split()[0]:
                    # first word
                    prev_positions = cur_positions
                else:
                    # not first word, check with previous words' position
                    temp_positions = []
                    for prev_position in prev_positions:
                        if prev_position + 1 in cur_positions:
                            temp_positions.append(prev_position + 1)
                    prev_positions = temp_positions

            freq = len(prev_positions)     

            if freq > max_freq:
                max_freq = freq
            phrase_frequency[doc_id][phrase] = freq        

    return phrase_frequency, max_freq



def calculate_similarity(query_term, query_phrase, body_index, title_index, body_weights, title_weights, FAVOR, doc_num):
    # tf_idf_weights: a dictionary. key: term, value: dictionary,  {doc_id: tf-idf_weight}

    query_term = indexer.stem(query_term, False)
    query_phrase = indexer.stem(query_phrase, True)
    print("stemmed query_term: ", query_term)
    print("stemmed query_phrase: ", query_phrase)

    all_terms = set(body_weights.keys()).union(set(title_weights.keys())).union(set(query_term)).union(set(query_phrase))

    query_vector = {term: 0 for term in all_terms}
    for term in query_term + query_phrase:
        query_vector[term] = 1
    

    doc_vectors = [{term: 0 for term in all_terms} for i in range(doc_num)]

    # 1. check if doc with each of the phrases
    phrases_freq_body, max_freq_body = count_phrase(body_index, query_phrase, doc_num)
    phrases_freq_title, max_freq_title = count_phrase(title_index, query_phrase, doc_num)
    print("phrases_freq_body: ", phrases_freq_body)
    print("phrases_freq_title: ", phrases_freq_title)


    # Calculate the total frequency of a certain phrase in every doc and use it to calculate weight
    phrase_weight_body = set_phrases_weight(body_weights, phrases_freq_body, max_freq_body)
    phrase_weight_title = set_phrases_weight(title_weights, phrases_freq_title, max_freq_title)
    print("phrase_weight_body: ", phrase_weight_body)
    print("phrase_weight_title: ", phrase_weight_title)

    for doc_id in range(doc_num):
        for term in all_terms:
            # 1. put phrase into the vector
            if term in query_phrase:
                doc_vectors[doc_id][term] += phrase_weight_body[doc_id][term]
                doc_vectors[doc_id][term] += phrase_weight_title[doc_id][term] * FAVOR
            # 2. put body term into the vector
            elif term in body_weights.keys() and doc_id in body_weights[term].keys():
                weight_dict = body_weights[term]
                doc_vectors[doc_id][term] += weight_dict[doc_id]
            # 3. put title term into the vector
            elif term in title_weights.keys() and doc_id in title_weights[term].keys():
                weight_dict = title_weights[term]
                doc_vectors[doc_id][term] += weight_dict[doc_id] * FAVOR

    # Convert query_vector and doc_vectors to matrices
    query_matrix = [list(query_vector.values())]
    doc_matrix = [list(doc_vector.values()) for doc_vector in doc_vectors]

    # Calculate cosine similarity
    docs_similarity = []
    for doc_id in range(len(doc_vectors)):
        doc_vector = doc_matrix[doc_id]
        doc_vector = numpy.array(doc_vector).reshape(1, -1)
        score = cosine_similarity(query_matrix, doc_vector)[0][0]
        docs_similarity.append((doc_id, score))
        
 
    return docs_similarity




def retrieval_function(query_term, query_phrase, body_index, title_index, max_pages, FAVOR=1.5):
    # FAVOR: a constant to boost the rank of a page if there is a match in the title

    # the weights are nested dictionary containing weights
    # outer dictionary - key: term  value: inner dictionary
    # inner dictionary - key: doc_id value: tfxidf weight
    print("body_index: ", body_index)
    print("title_index: ", title_index)
    body_weights = calculate_tfxidf(body_index, max_pages)
    title_weights = calculate_tfxidf(title_index, max_pages)

    # docs_similarity: a list of tuples - (doc_id, cosine similarity)
    docs_similarity = calculate_similarity(query_term, query_phrase, body_index, title_index, body_weights, title_weights, FAVOR, max_pages)
    print("docs_similarity: ", docs_similarity)
    result = sorted(docs_similarity, key=lambda x: x[1], reverse=True)    
    if(len(result) > 50):
        result = result[:50]

    for doc_id, score in result:
        print("doc_id: ", doc_id, "score: ", score)
    with open("result.txt", 'w') as file:
        for doc_id, score in result:
            file.write("doc_id: " + str(doc_id) + " score: " + str(score) + "\n")
    
    return result


# There is no need to calculate the weights of phrases and we can just hardcode the them