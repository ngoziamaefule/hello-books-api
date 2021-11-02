from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET", "POST"])
def handle_books():
    if request.method == "GET":
        title_query = request.args.get("title")
        
        if title_query:
            books = Book.query.filter_by(title=title_query)
        else:
            books = Book.query.all()

        books_response = []

        for book in books:
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
            )
        return jsonify(books_response)

    elif request.method == "POST":
        request_body = request.get_json()

        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"]
            )

        db.session.add(new_book)
        db.session.commit()

        return jsonify(f"Book {new_book.title} successfully created"), 201

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"])
def handle_book(book_id):
    book_id = int(book_id)
    book = Book.query.get(book_id)
    
    if book is None:
        return make_response(f"Book {book_id} not found", 404)

    if request.method == "GET":
        book_dict = {}
        if book_id == book.id:
            book_dict = {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        return jsonify(book_dict)

    elif request.method == "PUT":
        form_data = request.get_json()

        book.title = form_data["title"]
        book.description = form_data["description"]

        db.session.commit()

        return jsonify(f"Book #{book.id} successfully updated"), 200

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify(f"Book #{book.id} successfully deleted"), 200

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantasy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
# ] 

# books_bp = Blueprint("books", __name__, url_prefix="/books")

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)

# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     book_id = int(book_id)
#     for book in books:
#         if book.id == book_id:
#             return {
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description
#             }