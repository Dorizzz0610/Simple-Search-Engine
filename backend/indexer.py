from nltk.stem.porter import PorterStemmer 
from collections import defaultdict
import crawler

# An indexer which extracts keywords from a page and inserts them into an inverted file

# - The indexer first removes all stop words from the file; a dictionary of stop words will be provided
# - It then transforms words into stems using the Porter’s algorithm
# - It inserts the stems into the two inverted files:
#     - all stems extracted from the page body, together with all statistical information needed to support the vector space model (i.e., no need to support Boolean operations), are inserted into one inverted file
#     - all stems extracted from the page title are inserted into another inverted file
# - The indexes must be able to support phrase search such as “hong kong” in page titles and page bodies.


def remove_stopwords(words):
    STOPWORDS = set()
    with open('.\stopwords.txt', 'r') as file:
        for line in file:
            word = line.strip()
            if word:
                STOPWORDS.add(word)

    filtered_words = []
    for word in words:
        if word not in STOPWORDS:
            filtered_words.append(word)
    return filtered_words



def stem(words):
    stopwords = set(line.strip() for line in open('stopwords.txt')) 

    stemmer = PorterStemmer() 

    stemmed_words = [] 
    for word in words: 
        stemmed_word = stemmer.stem(word) 
        if stemmed_word not in stopwords: 
            stemmed_words.append(stemmed_word) 
    return stemmed_words


# def adding_phrase_to_index(query, query_phrase_position, index):
#     for phrase_info in query_phrase_position:
#         phrase = query[phrase_info[2]]
#         words_info_list = []
#         for i, word in enumerate(phrase):
#             if(word not in index):
#                 # the phrase isn't in the index
#                 break
#             words_info_list.append(index[word])
#         # the phrase is in the index
        
#         for word in phrase:
#             words_info_list.append(index[word])
                
#     return index          
                

def indexing(crawled_result):
    # indexing the keywords and body of a set of crawled pages    
    body_index = defaultdict(list)
    title_index = defaultdict(list)

    for page in crawled_result:
        original_title = page["title"].split() # a list of strings
        original_body = list(page["keywords"].keys()) # a list of strings

        original_title = remove_stopwords([word.lower() for word in original_title])
        original_body = remove_stopwords([word.lower() for word in original_body])

        title = stem(original_title)
        body = stem(original_body)
        

        # insert into title_index

        title_keywords_dict = crawler.extract_keywords(original_title)
        for i in range(len(title)):
            original_title_word = original_title[i]
            title_word = title[i]
            if(title_word not in title_index):
                title_index[title_word].append([page["page_id"], title_keywords_dict[original_title_word]["frequency"], title_keywords_dict[original_title_word]["positions"]])
            else:
                record_list = title_index[title_word]
                page_found = False
                for record in record_list:
                    if(record[0] == page["page_id"]):
                        record[1] += title_keywords_dict[original_title_word]["frequency"]
                        record[2].extend(title_keywords_dict[original_title_word]["positions"])
                        page_found = True
                        break
                if(not page_found):
                    title_index[title_word].append([page["page_id"], title_keywords_dict[original_title_word]["frequency"], title_keywords_dict[original_title_word]["positions"]])

        # insert into body_index

        body_keywords_dict = crawler.extract_keywords(original_body)
        for i in range(len(body)):
            original_body_word = original_body[i]
            body_word = body[i]
            if(body_word not in body_index):
                body_index[body_word].append([page["page_id"], body_keywords_dict[original_body_word]["frequency"], body_keywords_dict[original_body_word]["positions"]])
            else:
                record_list = body_index[body_word]
                page_found = False
                for record in record_list:
                    if(record[0] == page["page_id"]):
                        record[1] += body_keywords_dict[original_body_word]["frequency"]
                        record[2].extend(body_keywords_dict[original_body_word]["positions"])
                        page_found = True
                        break
                if(not page_found):
                    body_index[body_word].append([page["page_id"], body_keywords_dict[original_body_word]["frequency"], body_keywords_dict[original_body_word]["positions"]])

    # body_index = adding_phrase_to_index(query, query_phrase_position, body_index)
    # title_index = adding_phrase_to_index(query, query_phrase_position, title_index)

    with open('keyword.txt', 'w') as file:
        for(word, page_list) in body_index.items():
            for page in page_list:
                    file.write("word: " + word + " page: " + str(page[0]) + " count: " + str(page[1]) + "positions: " + str(page[2]) + "\n")
    return body_index, title_index



