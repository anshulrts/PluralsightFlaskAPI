from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {
        'name': "Outliers",
        'price': 7.88,
        'isbn': 9875789968
    },
    {
        'name': "Fame",
        'price': 3.45,
        'isbn': 675549968
    }
]

@app.route('/books')
def get_books():
    return jsonify({'books':books})

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        return "True"
    else:
        return "False"

def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

app.run(port=5000)