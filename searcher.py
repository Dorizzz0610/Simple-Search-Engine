import indexer
import crawler

def main():
    url = "https://shaw-auditorium.hkust.edu.hk/"
    MAX_PAGES = 50
    keyword_index, title_index = indexer.indexing({}, {}, url, MAX_PAGES)


    
    inverted_index = crawler.crawl(url, MAX_PAGES)
    crawler.create_txt(inverted_index, 'spider result.txt')
    crawler.database.export_tables()
    
    #print_pages(inverted_index)
    

if __name__ == "__main__":
    main()