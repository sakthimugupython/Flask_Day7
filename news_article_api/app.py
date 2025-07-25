from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

articles = []
article_id_counter = 1

class ArticleListResource(Resource):
    def get(self):
        category = request.args.get('category')
        published_date = request.args.get('published_date')
        filtered = articles
        if category:
            filtered = [a for a in filtered if a.get('category', '').lower() == category.lower()]
        if published_date:
            filtered = [a for a in filtered if a.get('published_date', '') == published_date]
        return {"articles": filtered}, 200

    def post(self):
        global article_id_counter
        data = request.get_json()
        if not data.get("headline") or not data.get("category") or not data.get("published_date"):
            return {"message": "Headline, category, and published_date are required."}, 400
        # Optionally validate published_date format
        try:
            datetime.strptime(data["published_date"], "%Y-%m-%d")
        except ValueError:
            return {"message": "published_date must be YYYY-MM-DD."}, 400
        new_article = {
            "id": article_id_counter,
            "headline": data["headline"],
            "category": data["category"],
            "published_date": data["published_date"]
        }
        articles.append(new_article)
        article_id_counter += 1
        return {"message": "Article created successfully", "article": new_article}, 201

class ArticleResource(Resource):
    def get(self, id):
        for article in articles:
            if article["id"] == id:
                return article, 200
        return {"message": "Article not found"}, 404

    def put(self, id):
        data = request.get_json()
        for article in articles:
            if article["id"] == id:
                if "headline" in data:
                    article["headline"] = data["headline"]
                if "category" in data:
                    article["category"] = data["category"]
                if "published_date" in data:
                    try:
                        datetime.strptime(data["published_date"], "%Y-%m-%d")
                        article["published_date"] = data["published_date"]
                    except ValueError:
                        return {"message": "published_date must be YYYY-MM-DD."}, 400
                return {"message": "Article updated", "article": article}, 200
        return {"message": "Article not found"}, 404

    def delete(self, id):
        for i, article in enumerate(articles):
            if article["id"] == id:
                articles.pop(i)
                return {"message": "Article deleted"}, 200
        return {"message": "Article not found"}, 404

api.add_resource(ArticleListResource, "/articles")
api.add_resource(ArticleResource, "/articles/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
