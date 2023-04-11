
def remove_stopwords(text):
    STOPWORDS = set(line.strip() for line in open('stopwords.txt'))


    filtered_words = []
    for word in text.split():
        if word not in STOPWORDS:
            filtered_words.append(word)

    print("Text after removing stopwords: ")
    print(" ".join(filtered_words))