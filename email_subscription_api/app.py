from flask import Flask, request
from flask_restful import Resource, Api
import re

app = Flask(__name__)
api = Api(app)

subscribers = set()
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class SubscribeResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        if not email or not re.match(EMAIL_REGEX, email):
            return {"message": "Invalid or missing email."}, 400
        subscribers.add(email)
        return {"message": f"{email} subscribed successfully."}, 201

class UnsubscribeResource(Resource):
    def delete(self, email):
        if email not in subscribers:
            return {"message": f"{email} is not subscribed."}, 404
        subscribers.remove(email)
        return {"message": f"{email} unsubscribed successfully."}, 200

api.add_resource(SubscribeResource, "/subscribe")
api.add_resource(UnsubscribeResource, "/subscribe/<string:email>")

if __name__ == '__main__':
    app.run(debug=True)
