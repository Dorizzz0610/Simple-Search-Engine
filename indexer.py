import crawler
import stopwords_remover
import stemmer


# An indexer which extracts keywords from a page and inserts them into an inverted file

# - The indexer first removes all stop words from the file; a dictionary of stop words will be provided
# - It then transforms words into stems using the Porter’s algorithm
# - It inserts the stems into the two inverted files:
#     - all stems extracted from the page body, together with all statistical information needed to support the vector space model (i.e., no need to support Boolean operations), are inserted into one inverted file
#     - all stems extracted from the page title are inserted into another inverted file
# - The indexes must be able to support phrase search such as “hong kong” in page titles and page bodies.


def indexing(keyword_index, title_index, url, max_pages):
    # indexing the keywords and body of a set of crawled pages
    
    crawled_result = crawler.crawl(url, max_pages)
    
    
    for url, page in crawled_result.items():
        title = page["title"]
        body = page["keywords"]
        
        title = stopwords_remover.remove_stopwords(title)
        body = stopwords_remover.remove_stopwords(body)

        title = stemmer.stemming(title)
        body = stemmer.stemming(body)

        title = list(set(title))
        body = list(set(body))

        title_index[url] = title
        keyword_index[url] = body

    return keyword_index, title_index
