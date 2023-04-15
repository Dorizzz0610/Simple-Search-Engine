import database
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import string


class Page:
    def __init__(self, id, title, last_modified, size, keywords, children, parents):
        self.id = id
        self.title = title
        self.last_modified = last_modified
        self.size = size
        self.keywords = keywords
        self.children = children
        self.parents = parents


# Get the response of HTTP request
def get_response(url):
    try:
        response = requests.get(url)
        return response
    except:
        return None

# Get the head of HTTP request
def get_head(url):
    try:
        head = requests.head(url)
        return head
    except:
        return None
    

# Extract the HTML content of the URL
def extract(url):
    response = get_response(url)
    response = response.text
    page = BeautifulSoup(response, 'html.parser')

    # Page title
    if(page.title):
        title = page.title.string.strip()
    else:
        title = ""

    # Last modified time
    head = get_head(url)
    last_modified = head.headers.get('Last-Modified')
    if last_modified is not None and last_modified > "":
        last_modified = last_modified
    else:
        last_modified = ""

    # Page size
    size = len(response)

    # Keywords and frequencies
    keywords = {}
    exclude = set(string.punctuation).union("|") # Set of punctuation marks
    word_id = 0
    for position, word in enumerate(page.get_text().split()):
        word = word.strip().lower()
        word = ''.join(ch for ch in word if ch not in exclude)
        if word in keywords:
            keywords[word]["frequency"] += 1
            keywords[word]["positions"].append(position)
        else:
            keywords[word] = {}
            keywords[word]["frequency"] = 1
            keywords[word]["word_id"] = word_id
            keywords[word]["positions"] = [position]
            word_id += 1

    # Children links in the page
    children = []
    for child in page.find_all('a'):
        child_link = child.get('href')
        if child_link and child_link.startswith('http'):
            if child_link not in children and child_link != url:
                children.append(child.get('href'))
    parents = []
    result = Page(-1, title, last_modified, size, keywords, children, parents) # -1 is just a placeholder
    return result


def store(crawled_result, url, page):
    
    if url in crawled_result and "last_modified" in crawled_result[url] and crawled_result[url]["last_modified"] != "":
        time1 = datetime.strptime(crawled_result[url]["last_modified"], "%a, %d %b %Y %H:%M:%S %Z")
        time2 = datetime.strptime(page.last_modified, "%a, %d %b %Y %H:%M:%S %Z")
        if time1 < time2: # if time1 is later
            return crawled_result
    
    database.insert_page(crawled_result, page, url)

    crawled_result[url] = {
            "page_id": page.id,
            "title": page.title,
            "last_modified": page.last_modified,
            "page_size": page.size,
            "keywords": page.keywords,
            "children": page.children,
            "parents": page.parents
        }
    
    return crawled_result

def crawl(url, max_pages):

    database.create_tables()

    crawl_list = [url]
    crawled_list = []
    count = 0

    crawled_result = {url: {}} #store parent->chidren

    while crawl_list and count < max_pages:
        current_url = crawl_list.pop(0)
        if current_url in crawled_list:
            continue
        if(get_response(current_url)):
            current_page = extract(current_url)
            current_page.id = count
            crawled_result[current_url] = {}
            crawled_result[current_url]["children"] = current_page.children
            if current_page.children:
                for child in current_page.children:
                    if child not in crawled_list and child not in crawl_list: #avoid cyclic?
                        crawl_list.append(child)

            crawled_list.append(current_url)
            count += 1
            crawled_result = store(crawled_result, current_url, current_page)

    for url in crawled_result:  
        if "children" in crawled_result[url]:
            for child in crawled_result[url]["children"]:
                if child in crawled_result.keys():
                    crawled_result[child]["parents"].append(url)
        
    
    return crawled_result


def print_pages(crawled_result):
    for url in crawled_result:
        print("URL: " + url)
        print("Title: " + crawled_result[url]["title"])
        print("Last modified: " + crawled_result[url]["last_modified"])
        print("Page size: " + str(crawled_result[url]["page_size"]))
        keys = list(crawled_result[url]["keywords"].keys())
        sliced_keys = keys[:10]
        sliced_keywords = {key: crawled_result[url]["keywords"][key] for key in sliced_keys}
        for key, value in sliced_keywords.items():
            print("\"" + key + "\"" + "(Word ID: " + str(value["word_id"]) + "): " + str(value["frequency"]) + "; ")
        for child in crawled_result[url]["children"]:
            if child in crawled_result:
                print("Child: " + str(crawled_result[child]['page_id']))
        print("")

def create_txt(crawled_result, file_name):
    with open(file_name, 'w') as file:
        for url in crawled_result:
            file.write("Page ID: " + str(crawled_result[url]["page_id"]) + "\n")
            file.write("Page title: " + crawled_result[url]["title"] + "\n")
            file.write("URL: " + url + "\n")
            file.write("Last modified: " + crawled_result[url]["last_modified"] + "    Page size: " + str(crawled_result[url]["page_size"]) + "\n")
            keys = list(crawled_result[url]["keywords"].keys())
            sliced_keys = keys[:10]
            sliced_keywords = {key: crawled_result[url]["keywords"][key] for key in sliced_keys}
            file.write("Keywords: ")
            for key, value in sliced_keywords.items():
                file.write("\"" + key + "\"" + "(Word ID: " + str(value["word_id"]) + "): " + str(value["frequency"]) + "; ")
            file.write("\n")
            count = 1
            for child in crawled_result[url]["children"]:
                if child in crawled_result.keys() and "page_id" in crawled_result[child].keys():
                    file.write("Child Link " + str(count) + ": " + child + " (page ID: " + str(crawled_result[child]["page_id"]) + ")")
                else:
                    file.write("Child Link " + str(count) + ": " + child)
                count += 1
                file.write("\n")
            file.write("\n")
            count = 1
            for parent in crawled_result[url]["parents"]:
                if parent in crawled_result.keys() and "page_id" in crawled_result[parent].keys():
                    file.write("Parent Link " + str(count) + ": " + parent + " (page ID: " + str(crawled_result[parent]["page_id"]) + ")\n")
                    count += 1
            file.write("\n")
            file.write("-------------------------------------------\n")



