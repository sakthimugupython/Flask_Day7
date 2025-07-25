from flask_restful import Resource, reqparse
from flask import request
from utils.response import ApiResponse

users = []
user_id_counter = 1

class UserResource(Resource):
    def get(self, user_id):
        user = next((u for u in users if u['id'] == user_id), None)
        if user:
            return ApiResponse(data=user)
        return ApiResponse(error="User not found", status=404)

    def put(self, user_id):
        global users
        data = request.get_json(silent=True)
        if not data:
            return ApiResponse(error="Missing JSON body", status=400)
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return ApiResponse(error="User not found", status=404)
        name = data.get('name', user['name'])
        email = data.get('email', user['email'])
        if email != user['email'] and any(u['email'] == email for u in users):
            return ApiResponse(error="Email already exists", status=400)
        user['name'] = name
        user['email'] = email
        return ApiResponse(data=user, message="User updated")

    def delete(self, user_id):
        global users
        user = next((u for u in users if u['id'] == user_id), None)
        if not user:
            return ApiResponse(error="User not found", status=404)
        users = [u for u in users if u['id'] != user_id]
        return ApiResponse(message="User deleted")

class UserListResource(Resource):
    def get(self):
        return ApiResponse(data=users)

    def post(self):
        global users, user_id_counter
        data = request.get_json(silent=True)
        if not data:
            return ApiResponse(error="Missing JSON body", status=400)
        name = data.get('name')
        email = data.get('email')
        if not name or not email:
            return ApiResponse(error="Name and email required", status=400)
        if any(u['email'] == email for u in users):
            return ApiResponse(error="Email already exists", status=400)
        new_user = {'id': user_id_counter, 'name': name, 'email': email}
        users.append(new_user)
        user_id_counter += 1
        return ApiResponse(data=new_user, message="User created", status=201)
