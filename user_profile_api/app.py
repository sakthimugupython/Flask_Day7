from flask import Flask, request
from flask_restful import Resource, Api

users = []
user_id_counter = 1

app = Flask(__name__)
api = Api(app)

class UserList(Resource):
    def get(self):
        return {"users": users}, 200

    def post(self):
        global user_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("email"):
            return {"message": "Name and Email are required."}, 400

        new_user = {
            "id": user_id_counter,
            "name": data["name"],
            "email": data["email"]
        }
        users.append(new_user)
        user_id_counter += 1
        return {"message": "User created successfully", "user": new_user}, 201

class User(Resource):
    def get(self, id):
        for user in users:
            if user["id"] == id:
                return user, 200
        return {"message": "User not found"}, 404

    def put(self, id):
        data = request.get_json()
        for user in users:
            if user["id"] == id:
                user["name"] = data.get("name", user["name"])
                user["email"] = data.get("email", user["email"])
                return {"message": "User updated", "user": user}, 200
        return {"message": "User not found"}, 404

    def delete(self, id):
        for i, user in enumerate(users):
            if user["id"] == id:
                users.pop(i)
                return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404

api.add_resource(UserList, "/users")
api.add_resource(User, "/users/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
