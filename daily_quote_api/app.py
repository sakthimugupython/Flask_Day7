from flask import Flask, request
from flask_restful import Resource, Api
import random

app = Flask(__name__)
api = Api(app)

quotes = []
quote_id_counter = 1

class QuoteListResource(Resource):
    def get(self):
        return {"quotes": quotes}, 200

    def post(self):
        global quote_id_counter
        data = request.get_json()
        if not data.get("text") or not data.get("author"):
            return {"message": "Quote text and author are required."}, 400
        new_quote = {
            "id": quote_id_counter,
            "text": data["text"],
            "author": data["author"]
        }
        quotes.append(new_quote)
        quote_id_counter += 1
        return {"message": "Quote added successfully", "quote": new_quote}, 201

class QuoteResource(Resource):
    def get(self, id):
        for quote in quotes:
            if quote["id"] == id:
                return quote, 200
        return {"message": "Quote not found"}, 404

    def put(self, id):
        data = request.get_json()
        for quote in quotes:
            if quote["id"] == id:
                if "text" in data:
                    quote["text"] = data["text"]
                if "author" in data:
                    quote["author"] = data["author"]
                return {"message": "Quote updated", "quote": quote}, 200
        return {"message": "Quote not found"}, 404

    def delete(self, id):
        for i, quote in enumerate(quotes):
            if quote["id"] == id:
                quotes.pop(i)
                return {"message": "Quote deleted"}, 200
        return {"message": "Quote not found"}, 404

class RandomQuoteResource(Resource):
    def get(self):
        if not quotes:
            return {"message": "No quotes available."}, 404
        return random.choice(quotes), 200

api.add_resource(QuoteListResource, "/quotes")
api.add_resource(QuoteResource, "/quotes/<int:id>")
api.add_resource(RandomQuoteResource, "/quotes/random")

if __name__ == '__main__':
    app.run(debug=True)
