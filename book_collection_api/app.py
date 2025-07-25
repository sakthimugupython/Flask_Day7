from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

books = []
book_id_counter = 1

class BookListResource(Resource):
    def get(self):
        author = request.args.get('author')
        filtered_books = books
        if author:
            filtered_books = [b for b in books if b.get('author', '').lower() == author.lower()]
        return {"books": filtered_books}, 200

    def post(self):
        global book_id_counter
        data = request.get_json()
        if not data.get("title") or not data.get("author") or not data.get("year"):
            return {"message": "Title, author, and year are required."}, 400
        new_book = {
            "id": book_id_counter,
            "title": data["title"],
            "author": data["author"],
            "year": data["year"]
        }
        books.append(new_book)
        book_id_counter += 1
        return {"message": "Book added successfully", "book": new_book}, 201

class BookResource(Resource):
    def get(self, id):
        for book in books:
            if book["id"] == id:
                return book, 200
        return {"message": "Book not found"}, 404

    def put(self, id):
        data = request.get_json()
        for book in books:
            if book["id"] == id:
                if "title" in data:
                    book["title"] = data["title"]
                if "author" in data:
                    book["author"] = data["author"]
                if "year" in data:
                    book["year"] = data["year"]
                return {"message": "Book updated", "book": book}, 200
        return {"message": "Book not found"}, 404

    def delete(self, id):
        for i, book in enumerate(books):
            if book["id"] == id:
                books.pop(i)
                return {"message": "Book deleted"}, 200
        return {"message": "Book not found"}, 404

api.add_resource(BookListResource, "/books")
api.add_resource(BookResource, "/books/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
