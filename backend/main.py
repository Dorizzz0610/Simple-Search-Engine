from collections import defaultdict
import indexer
import crawler
import searcher

def main():
    starting_url = "https://cse.hkust.edu.hk"
    MAX_PAGES = 20
    

    query = input("Enter your query: ")
    query = query.split()

    # Step 1: Crawl the pages
    print("Crawling the pages...")
    crawled_result = crawler.crawl(starting_url, MAX_PAGES)
    for url, page in crawled_result.items():
        keywords = page["keywords"]
        print("URL: " + url + " Keywords: " + str(keywords))

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
    # crawler.create_txt(inverted_index, 'spider result.txt')
    # crawler.database.export_tables()
    
    

if __name__ == "__main__":
    main()