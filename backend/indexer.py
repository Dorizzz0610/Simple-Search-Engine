from nltk.stem.porter import PorterStemmer 

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


def preprocess(text):
    text = [word.lower() for word in text]
    text = remove_stopwords(text)
    text = stem(text)
    text = list(set(text)) # remove duplicates
    return text


def get_phrases(text):
    phrases = []
    for i in range(len(text)-1):
        phrases.append(text[i] + " " + text[i+1])
    return phrases




def indexing(keyword_index, title_index, crawled_result):
    # indexing the keywords and body of a set of crawled pages    
    
    for page in crawled_result.values():
        title = page["title"].split() # a list of strings
        body = list(page["keywords"].keys()) # a list of strings

        # stem and remove stopwords
        title = preprocess(title)
        body = preprocess(body)
        
        # handle searchs containing phrases
        title_phrases = get_phrases(title)
        body_phrases = get_phrases(body)

        # insert into title_index
        for title_word in title:
            if title_word not in title_index.keys():
                title_index[title_word].append((page["page_id"], title.count(title_word)))
        for title_phrase in title_phrases:
            if title_phrase not in title_index.keys():
                title_index[title_phrase].append((page["page_id"], title_phrases.count(title_phrase)))

        # insert into keyword_index
        for body_word in body:
            keyword_index[body_word].append((page["page_id"], body.count(body_word)))
        for body_phrase in body_phrases:
            keyword_index[body_phrase].append((page["page_id"], body_phrases.count(body_phrase)))
        

    return keyword_index, title_index



