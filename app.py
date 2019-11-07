from flask import Flask, jsonify

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

app.run(port=5000)