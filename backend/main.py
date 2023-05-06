import indexer
import crawler
import searcher


def handle_query(query):
    single_terms = []
    phrases = []

    in_phrase = False
    current_phrase = ""
    current_term = ""

    for i in query:
        if i == '"':
            if in_phrase:
                phrases.append(current_phrase)
                current_phrase = ""
                in_phrase = False
            else:
                in_phrase = True
                if current_term:
                    single_terms.append(current_term)
                    current_term = ""
        elif i == " ":
            if in_phrase:
                current_phrase += i
            else:
                if current_term:
                    single_terms.append(current_term)
                    current_term = ""
        else:
            if in_phrase:
                current_phrase += i
            else:
                current_term += i

    if current_term:
        single_terms.append(current_term)
    if current_phrase:
        phrases.append(current_phrase)


    return single_terms, phrases


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
    MAX_PAGES = 30
    
    # Step 0: Get the query
    query = input("Enter your query: ")
    query_term, query_phrase = handle_query(query)

    print(query_term)
    print(query_phrase)


    # Step 1: Crawl the pages
    print("Crawling the pages...")
    crawled_result = crawler.crawl(starting_url, MAX_PAGES) # store based on id 


    # Step 2: Index the crawled pages
    print("Indexing the pages...")


    body_index, title_index = indexer.indexing(crawled_result)


    # Step 3: Search the query
    print("Searching the query...")
    search_result = searcher.retrieval_function(query_term, query_phrase, body_index, title_index, MAX_PAGES, 1.5)
    


    # inverted_index = crawler.crawl(starting_url, MAX_PAGES)
    crawler.create_txt(crawled_result, 'spider result.txt')
    # crawler.database.export_tables()
    
    

if __name__ == "__main__":
    main()


