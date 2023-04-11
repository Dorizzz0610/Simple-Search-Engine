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


def indexing(url, max_pages):
    crawled_result = crawler.crawl(url, max_pages)

