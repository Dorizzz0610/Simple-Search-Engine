from collections import defaultdict
import indexer
import crawler
import searcher

def main():
    starting_url = "https://shaw-auditorium.hkust.edu.hk/"
    MAX_PAGES = 50

    query = input("Enter your query: ")
    query = query.split()


    keyword_index = defaultdict(list)
    title_index = defaultdict(list)

    keyword_index, title_index = indexer.indexing(keyword_index, title_index, starting_url, MAX_PAGES)

    top_doc = searcher.retrieval_function(query, keyword_index, title_index)
    
    inverted_index = crawler.crawl(starting_url, MAX_PAGES)
    crawler.create_txt(inverted_index, 'spider result.txt')
    crawler.database.export_tables()
    
    #print_pages(inverted_index)
    

if __name__ == "__main__":
    main()