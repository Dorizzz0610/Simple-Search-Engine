import indexer
import crawler
import searcher
import database
import json
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask_socketio import SocketIO, emit
from flask_cors import CORS


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

def replace_chars(str):
    str = str.replace('\n', '<br>')
    str = str.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;') # use 4 spaces for each tab
    return str

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])

def search():
    data = request.get_json()
    print(data)

    query = data['query']
    starting_url = data['startingURL']
    max_pages = int(data['maxPages'])

    results = main(query, starting_url, max_pages)
    
    return jsonify(results)


def main(query, starting_url, MAX_PAGES):
    print(query)
    #starting_url = "https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm"
    #starting_url = "https://cse.hkust.edu.hk/"
    #MAX_PAGES = 5
    
    # Step 0: Get the query
    #query = input("Enter your query: ")
    query_term, query_phrase = handle_query(query)

    print(query_term)
    print(query_phrase)


    # Step 1: Crawl the pages
    print("Crawling the pages...")
    crawled_result = crawler.crawl(starting_url, MAX_PAGES) # store based on id 
    print(crawled_result)


    # Step 2: Index the crawled pages
    print("Indexing the pages...")


    body_index, title_index = indexer.indexing(crawled_result)
    print(body_index)
    database.export_tables()


    # Step 3: Search the query
    print("Searching the query...")
    search_result = searcher.retrieval_function(query_term, query_phrase, body_index, title_index, MAX_PAGES, 1.5)
    
    result_front_end = []

    for doc_id, score in search_result:
        current_result = []
        current_result.append("Score: " + str(score) + "    " + crawled_result[doc_id]["title"])
        current_result.append("  URL: " + crawled_result[doc_id]["url"])

        current_result.append("  " + "Last modified time: " + crawled_result[doc_id]["last_modified"] + ", Page size: " + str(crawled_result[doc_id]["page_size"]) + '\n')
        
        top_n_words = crawler.top_n_keywords(crawled_result[doc_id]["keywords"], 5)
        top_n_words_str = "  Top 5 keywords: "
        for word in top_n_words:
            top_n_words_str += (word + " " + str(crawled_result[doc_id]["keywords"][word]["frequency"]) + "; ")
        current_result.append(top_n_words_str + '\n')

        current_result.append("  Parent links: ")
        count = 0
        for parent in crawled_result[doc_id]["parents"]:
            current_result.append("    " + parent)
            count += 1
            if count == 5:
                current_result.append("    ......\n")
                break

        current_result.append("  Children links: ")
        count = 0
        for child in crawled_result[doc_id]["children"]:
            current_result.append("    " + child)
            count += 1
            if count == 5:
                current_result.append("    ......\n")
                break
        current_result.append('\n')

        for string in current_result:
            string = replace_chars(string)
        result_front_end.append(current_result)

    print(result_front_end)
    print("length: ", len(result_front_end))
    print("========================Search End========================")
    return result_front_end


    


if __name__ == "__main__":
    app.run(debug=False, port=5000)


