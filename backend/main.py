from collections import defaultdict
import indexer
import crawler
import searcher

def main():
    starting_url = "https://cse.hkust.edu.hk"
    MAX_PAGES = 25
    
    # Step 0: Get the query
    query = input("Enter your query: ")
    words = query.split()

    in_phrase = False
    phrase = ""
    new_words = []
    for word in words:
        if word.startswith('"'):
            in_phrase = True
            phrase = word[1:]
        elif in_phrase:
            phrase += " " + word
            if word.endswith('"'):
                new_words.append(phrase[:-1])
                in_phrase = False
        else:
            new_words.append(word)
    query = new_words
    # query is now a list. Each element is either a word or a phrase
    print(query)


    # Step 1: Crawl the pages
    print("Crawling the pages...")
    crawled_result = crawler.crawl(starting_url, MAX_PAGES)

    # Step 2: Index the crawled pages
    print("Indexing the pages...")
    keyword_index = defaultdict(list)
    title_index = defaultdict(list)

    keyword_index, title_index = indexer.indexing(keyword_index, title_index, crawled_result)

    # Step 3: Search the query
    print("Searching the query...")
    top_doc = searcher.retrieval_function(query, keyword_index, title_index, MAX_PAGES, 1.5)

    print("The best fit page is: " + str(top_doc))
    


    # inverted_index = crawler.crawl(starting_url, MAX_PAGES)
    crawler.create_txt(crawled_result, 'spider result.txt')
    # crawler.database.export_tables()
    
    

if __name__ == "__main__":
    main()