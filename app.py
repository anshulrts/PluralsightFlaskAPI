from flask import Flask, jsonify, request, Response
import json

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
        response = Response("", 201, mimetype="application/json")
        response.location = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid Book Object passed in the request",
            "helpString": "Data passed in similar to this { 'name': 'bookname', 'price': 7.99, 'isbn': 783276234 }"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), 400, mimetype='application/json')
        return response


def validBookObject(bookObject):
    if("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False


# PUT Request
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    req = request.get_json()
    new_book = {
        "name": req['name'],
        "price": req['price']
    }

    i = 0
    for book in books:
        if isbn == book['isbn']:
            books[i] = new_book
        i += 1
    
    response = Response("", status=204)
    return response


# PATCH Request - Just to update a part of Object. For e.g only Name/Price
@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}

    if "name" in request_data:
        updated_book['name'] = request_data['name']
    if "price" in request_data:
        updated_book['price'] = request_data['price']

    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


# Delete Request
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    i = 0
    for book in books:
        if book['isbn'] == isbn:
            books.pop(i)
            response = Response("", status = 204)
            return response
        i += 1
    
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
    }

    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    return response

app.run(port=5000)