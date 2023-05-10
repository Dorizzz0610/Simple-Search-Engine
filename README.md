# Simple-Search-Engine


A simple search engine starting from a specific website.

### Query format
* a string
* allows phrases to be specified in double quotation marks
* search for logical operators aren't supported yet

### Tech stack
- Back-end: Python
- Database: MySQL
- Front-end: React.js

### Overall design
In the backend part, there are the following parts:
1. crawler
2. indexer
3. searcher
4. main function to handle query and interact with the frontend

### Test

You need to first manually install Python, MySQL Workbench, Node.js and React on your OS.

To make communication between the Python backend and React frontend work properly, you need to run two applications simultaneously: the Python backend and the React frontend. In this case, the Python backend will act as the WebSocket server, while the React frontend will act as the WebSocket client. The Python backend and React frontend will run on different ports so that they can communicate with each other. We will use port 3000 for the frontend and port 5000 for the backend.

Usually, during development, you need to run both applications at the same time, so you need to open two terminal windows, one for starting the Python backend and the other for starting the React frontend. This have already been written in a script in `start_windows.bat` and `start_linux.sh`.

Overall steps for Windows users:

1. If you want to test with storing the data into database, open MySQL, create a connection with following details:
    
    ```python
    host="localhost",
    user="COMP4321",
    password="COMP4321Crawler",
    database="CrawlerDB"
    ```
    
    And in the very beginning part of `main.py`, set:
    
    ```python
    DATABASE = True
    ```
    
    If you want to test without database,  in `main.py`, leave:
    
    ```python
    DATABASE = False
    ```
    
2. cd to the project directory
3. run `./setup_windows.bat` to install the packages in requirement.txt
4. run `./start_windows.bat` to start the frontend and backend terminal
5. type the search detail in the React APP opened in the browser
6. check the search result on the web page returned by the backend
7. refresh the page for the next search

Similarly, overall steps for Linux users:

1. If you want to test with storing the data into database, open MySQL, create a connection with following details:
    
    ```python
    host="localhost",
    user="COMP4321",
    password="COMP4321Crawler",
    database="CrawlerDB"
    ```
    
    And in the very beginning part of `main.py`, set:
    
    ```python
    DATABASE = True
    ```
    
    If you want to test without database,  in `main.py`, leave:
    
    ```python
    DATABASE = False
    ```
    
2. cd to the project directory
3. run `./setup_linux.sh` to install the packages in requirement.txt
4. run `./start_linux.sh` to start the frontend and backend terminal
5. type the search detail in the React APP opened in the browser
6. check the search result on the web page returned by the backend
7. refresh the page for the next search

The testing example can be checked in the demo video: [https://www.youtube.com/watch?v=yMpu9aMGSoA&ab_channel=DorisZhang]
