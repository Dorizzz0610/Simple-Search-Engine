from nltk.stem.porter import PorterStemmer 
from nltk.tokenize import word_tokenize


def stemming(tokenized_text):
    stopwords = set(line.strip() for line in open('stopwords.txt')) 

    stemmer = PorterStemmer() 

    stemmed_words = [] 
    for word in tokenized_text: 
        stemmed_word = stemmer.stem(word) 
        if stemmed_word not in stopwords: 
            stemmed_words.append(stemmed_word) 

    print(stemmed_words)
    # ['fish', 'fish', 'fish', 'fish'] 