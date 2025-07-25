from flask import Flask
from flask_restful import Api
import os

app = Flask(__name__)
api = Api(app)

# Import resources after app and api are created
from resources.user import UserResource, UserListResource

# Add resource routes
api.add_resource(UserResource, '/api/user/<int:user_id>')
api.add_resource(UserListResource, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)
