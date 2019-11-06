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

app.run(port=5000)