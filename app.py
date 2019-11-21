from flask import Flask, jsonify, request, Response
import json
from BookModel import *
from settings import *

import jwt, datetime
from UserModel import User

app.config['SECRET_KEY'] = 'meow'

@app.route('/login', methods=['POST'])
def get_token():

    request_body = request.get_json()
    username = request_body['username']
    password = request_body['password']

    match = User.username_password_match(username, password)

    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({'exp': expiration_date}, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    else:
        return Response("", 401, mimetype='application/json')

@app.route('/books')
def get_books():
    token = request.args.get('token')

    try:
        jwt.decode(token, app.config['SECRET_KEY'])
    except:
        return jsonify({ 'error' : 'Need a valid token to view this page' }), 401
    
    return jsonify({ 'books': Book.get_all_books() })


@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = Book.get_book(isbn)
    return jsonify(return_value)


@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype="application/json")
        response.location = "/books/" + str(request_data['isbn'])
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
    # new_book = {
    #     "name": req['name'],
    #     "price": req['price']
    # }

    # i = 0
    # for book in books:
    #     if isbn == book['isbn']:
    #         books[i] = new_book
    #     i += 1

    Book.replace_book(isbn, req['name'], req['price'])
    
    response = Response("", status=204)
    return response


# PATCH Request - Just to update a part of Object. For e.g only Name/Price
@app.route("/books/<int:isbn>", methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}

    if "name" in request_data:
        Book.update_book_name(isbn, request_data['name'])
    if "price" in request_data:
        Book.update_book_price(isbn, request_data['price'])
    
    response = Response("", status=204)
    response.headers['Location'] = '/books/' + str(isbn)
    return response


# Delete Request
@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    is_successful = Book.delete_book(isbn)
    
    if(is_successful):
        response = Response("", status=204)
        return response
    
    invalidBookObjectErrorMsg = {
        "error": "Book with the ISBN number that was provided was not found, so therefore unable to delete"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype='application/json')
    
    return response

app.run(port=5000)