from flask import Flask, request

app = Flask(__name__)

@app.route('/search', methods=['POST'])
def search():
    search_text = request.json.get('searchText')
    return search_text