import indexer
import crawler
from collections import defaultdict


def retrieval_function():
    # A retrieval function (or called the **search engine**) that compares a list of query terms against the inverted file and returns the top documents, 
    # up to a maximum of 50, to the user in a ranked order according to the vector space model. As noted about, phrase must be supported, e.g., “hong kong” universities
    #     - Term weighting formula is based on tfxidf/max(tf) and document similarity is based on cosine similarity measure.
    #     - Derive and implement a mechanism to favor matches in title. For example, a match in the title would significantly boost the rank of a page
    pass



def main():
    starting_url = "https://shaw-auditorium.hkust.edu.hk/"
    MAX_PAGES = 50

    keyword_index = defaultdict(list)
    title_index = defaultdict(list)

    keyword_index, title_index = indexer.indexing(keyword_index, title_index, starting_url, MAX_PAGES)

    
    inverted_index = crawler.crawl(starting_url, MAX_PAGES)
    crawler.create_txt(inverted_index, 'spider result.txt')
    crawler.database.export_tables()
    
    #print_pages(inverted_index)
    

if __name__ == "__main__":
    main()