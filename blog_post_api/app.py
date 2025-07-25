from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

posts = []
post_id_counter = 1

class PostListResource(Resource):
    def get(self):
        return {"posts": posts}, 200

    def post(self):
        global post_id_counter
        data = request.get_json()
        if not data.get("title") or not data.get("content"):
            return {"message": "Title and Content are required."}, 400
        new_post = {
            "id": post_id_counter,
            "title": data["title"],
            "content": data["content"],
            "author": data.get("author", "")
        }
        posts.append(new_post)
        post_id_counter += 1
        return {"message": "Post created successfully", "post": new_post}, 201

class PostResource(Resource):
    def get(self, id):
        for post in posts:
            if post["id"] == id:
                return post, 200
        return {"message": "Post not found"}, 404

    def put(self, id):
        data = request.get_json()
        for post in posts:
            if post["id"] == id:
                if "title" in data:
                    post["title"] = data["title"]
                if "content" in data:
                    post["content"] = data["content"]
                if "author" in data:
                    post["author"] = data["author"]
                return {"message": "Post updated", "post": post}, 200
        return {"message": "Post not found"}, 404

    def delete(self, id):
        for i, post in enumerate(posts):
            if post["id"] == id:
                posts.pop(i)
                return {"message": "Post deleted"}, 200
        return {"message": "Post not found"}, 404

api.add_resource(PostListResource, "/posts")
api.add_resource(PostResource, "/posts/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
