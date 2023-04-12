import crawler
from nltk.stem.porter import PorterStemmer 

# An indexer which extracts keywords from a page and inserts them into an inverted file

# - The indexer first removes all stop words from the file; a dictionary of stop words will be provided
# - It then transforms words into stems using the Porter’s algorithm
# - It inserts the stems into the two inverted files:
#     - all stems extracted from the page body, together with all statistical information needed to support the vector space model (i.e., no need to support Boolean operations), are inserted into one inverted file
#     - all stems extracted from the page title are inserted into another inverted file
# - The indexes must be able to support phrase search such as “hong kong” in page titles and page bodies.




def remove_stopwords(text):
    STOPWORDS = set(line.strip() for line in open('stopwords.txt'))

    filtered_words = []
    for word in text:
        if word not in STOPWORDS:
            filtered_words.append(word)

    return filtered_words



def stem(text):
    stopwords = set(line.strip() for line in open('stopwords.txt')) 

    stemmer = PorterStemmer() 

    stemmed_words = [] 
    for word in text: 
        stemmed_word = stemmer.stem(word) 
        if stemmed_word not in stopwords: 
            stemmed_words.append(stemmed_word) 

    return stemmed_words


def preprocess(text):
    text = remove_stopwords(text)
    text = stem(text)
    text = list(set(text))
    return text


def get_phrases(text):
    phrases = []
    for i in range(len(text)-1):
        phrases.append(text[i] + " " + text[i+1])
    return phrases


def indexing(keyword_index, title_index, url, max_pages):
    # indexing the keywords and body of a set of crawled pages

    crawled_result = crawler.crawl(url, max_pages)
    
    
    for url, page in crawled_result.items():
        title = preprocess(page["title"]) # a string
        body = preprocess(page["keywords"]) # a dictionary
        

        title_index[url] = title
        keyword_index[url] = body

    return keyword_index, title_index
