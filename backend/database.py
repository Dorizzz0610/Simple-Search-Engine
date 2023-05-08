import mysql.connector
import subprocess

def create_tables():
    print("creating tables")
    connection = mysql.connector.connect(
        host="localhost",
        user="COMP4321",
        password="COMP4321Crawler",
        database="CrawlerDB"
    )

    cursor = connection.cursor()


    # SQL statement to create the relationship table
    create_relationship_table = """CREATE TABLE IF NOT EXISTS relationship (
                                page_id INT NOT NULL,
                                relationship TEXT NOT NULL,
                                other_URL TEXT NOT NULL,
                                other_page_id INT,
                                PRIMARY KEY (page_id, other_URL(700)),
                                UNIQUE KEY page_url_unique (page_id, other_URL)
                            )"""
    cursor.execute(create_relationship_table)

    # SQL statement to create the keywords table
    create_keywords_table = """CREATE TABLE IF NOT EXISTS keywords (
                                page_id INT,
                                word VARCHAR(255) NOT NULL,
                                word_id INT NOT NULL,
                                frequency INT NOT NULL,
                                PRIMARY KEY (page_id, word)
                            )"""
    cursor.execute(create_keywords_table)

    create_body_index_table = """CREATE TABLE IF NOT EXISTS title_index (
                            word VARCHAR(255) NOT NULL,
                            page_id INT NOT NULL,
                            frequency INT NOT NULL,
                            positions TEXT NOT NULL,
                            PRIMARY KEY (word, page_id)
                      )"""
    cursor.execute(create_body_index_table)

    create_title_index_table = """CREATE TABLE IF NOT EXISTS body_index (
                            word VARCHAR(255) NOT NULL,
                            page_id INT NOT NULL,
                            frequency INT NOT NULL,
                            positions TEXT NOT NULL,
                            PRIMARY KEY (word, page_id)
                      )"""
    cursor.execute(create_title_index_table)


    connection.commit()
    connection.close()



def insert_page(crawled_result, page, url):
    connection = mysql.connector.connect(
        host="localhost",
        user="COMP4321",
        password="COMP4321Crawler",
        database="CrawlerDB"
    )

    cursor =  connection.cursor()


    # Insert keywords and their frequencies into the keywords table and retrieve the corresponding word_id for each keyword
    insert_keywords = """
        REPLACE INTO keywords (page_id, word, frequency, word_id)
        VALUES (%s, %s, %s, %s)
    """
    keywords_insertion = []
    count = 0
    for word in page.keywords.keys():
        keywords_insertion.append([page.id, word, page.keywords[word]["frequency"], page.keywords[word]["word_id"]])
        count += 1
        if(count == 10): break
    cursor.executemany(insert_keywords, keywords_insertion)
    connection.commit()


    # Insert each child url into the children table
    for child_url in page.children:
        child_id = None
        if(child_url in crawled_result):
            child_id = crawled_result[child_url]["page_id"]
        if child_id is not None:
            cursor.execute("""
                INSERT IGNORE INTO relationship (page_id, relationship, other_URL, other_page_id)
                VALUES (%s, %s, %s, %s)
            """, (page.id, "PARENT", child_url, child_id))
        else:
            cursor.execute("""
                INSERT IGNORE INTO relationship (page_id, relationship, other_URL)
                VALUES (%s, %s, %s)
            """, (page.id, "PARENT", child_url))
        connection.commit()


    for parent_url in page.parents:
        parent_id = None
        if parent_url in crawled_result:  
            parent_id = crawled_result[parent_url]["page_id"]
        if parent_id is not None:
            cursor.execute("""
                INSERT IGNORE INTO relationship (page_id, relationship, other_URL, other_page_id)
                VALUES (%s, %s, %s, %s)
            """, (page.id, "CHILDREN", parent_url, parent_id))
        else:
            cursor.execute("""
                INSERT IGNORE INTO relationship (page_id, relationship, other_URL)
                VALUES (%s, %s, %s)
            """, (page.id, "CHILDREN", parent_url))
        connection.commit()

    connection.close()


def insert_index(body_index, title_index):
    connection = mysql.connector.connect(
        host="localhost",
        user="COMP4321",
        password="COMP4321Crawler",
        database="CrawlerDB"
    )
    cursor = connection.cursor()

    for word, page_list in body_index.items():
        for page in page_list:
            cursor.execute('''INSERT INTO body_index (word, page_id, frequency, positions)
                              VALUES (%s, %s, %s, %s)
                              ON DUPLICATE KEY UPDATE frequency = frequency + %s, positions = CONCAT_WS(',', positions, %s)''',
                           (word, page[0], page[1], ','.join(map(str, page[2])), page[1], ','.join(map(str, page[2]))))

    for word, page_list in title_index.items():
        for page in page_list:
            cursor.execute('''INSERT INTO title_index (word, page_id, frequency, positions)
                              VALUES (%s, %s, %s, %s)
                              ON DUPLICATE KEY UPDATE frequency = frequency + %s, positions = CONCAT_WS(',', positions, %s)''',
                           (word, page[0], page[1], ','.join(map(str, page[2])), page[1], ','.join(map(str, page[2]))))

    connection.commit()


def export_tables():

    config = {
        'user': 'COMP4321',
        'password': 'COMP4321Crawler',
        'database': 'CrawlerDB',
        'host': 'localhost'
    }

    cmd = ['mysqldump', '-u', config['user'], '-p'+config['password'], '--databases', config['database'], '--result-file', 'result.sql', '--no-create-info']
    subprocess.run(cmd)