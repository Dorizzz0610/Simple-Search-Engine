from collections import defaultdict
import indexer
import crawler
import searcher


def handle_query(query):
    words = query.split()

    in_phrase = False
    phrase = ""
    new_words = []
    phrase_position = []
    new_phrase_position = [] # elements: tuple (begin, end, index), index is the position of the phrase in new_words

    for i, word in enumerate(words):
        if word.startswith('"'):
            in_phrase = True
            phrase = word[1:]
            phrase_position.append((i,))
        elif in_phrase:
            phrase += " " + word
            if word.endswith('"'):
                new_words.append(phrase[:-1])
                start = phrase_position[-1][0]
                end = i
                phrase_position[-1] = (start, end)
                new_phrase_position.append((start, end, len(new_words)-1))
                in_phrase = False
            else:
                phrase_position[-1] = (phrase_position[-1][0], i)
        else:
            new_words.append(word)

    return new_words, new_phrase_position


def return_to_frontend(crawled_result, search_result):
    # TODO: change crawled_result with keys in page_id; change the codes used crawled_result; finish this function
    result = []
    for page_id, score in search_result:
        page = crawled_result[page_id]
        result.append({
            "title": page["title"],
            "url": page["url"],
            "body": page["body"]
        })
    return result


def main():
    starting_url = "https://cse.hkust.edu.hk"
    MAX_PAGES = 10
    
    # Step 0: Get the query
    query = input("Enter your query: ")
    query, query_phrase_position = handle_query(query)

    # query is now a list. Each element is either a word or a phrase
    print(query)
    print(query_phrase_position)


    # Step 1: Crawl the pages
    print("Crawling the pages...")
    crawled_result = crawler.crawl(starting_url, MAX_PAGES)


    # Step 2: Index the crawled pages
    print("Indexing the pages...")
    body_index = defaultdict(list)
    title_index = defaultdict(list)

    body_index, title_index = indexer.indexing(body_index, title_index, crawled_result)


    # Step 3: Search the query
    print("Searching the query...")
    search_result = searcher.retrieval_function(query, query_phrase_position, body_index, title_index, MAX_PAGES, 1.5)
    


    # inverted_index = crawler.crawl(starting_url, MAX_PAGES)
    crawler.create_txt(crawled_result, 'spider result.txt')
    # crawler.database.export_tables()
    
    

if __name__ == "__main__":
    main()


