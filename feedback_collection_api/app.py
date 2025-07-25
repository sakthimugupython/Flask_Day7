from flask import Flask, request
from flask_restful import Resource, Api
import re

app = Flask(__name__)
api = Api(app)

feedbacks = []
feedback_id_counter = 1
EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class FeedbackListResource(Resource):
    def post(self):
        global feedback_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("email") or not data.get("message"):
            return {"message": "Name, email, and message are required."}, 400
        if not re.match(EMAIL_REGEX, data["email"]):
            return {"message": "Invalid email format."}, 400
        new_feedback = {
            "id": feedback_id_counter,
            "name": data["name"],
            "email": data["email"],
            "message": data["message"]
        }
        feedbacks.append(new_feedback)
        feedback_id_counter += 1
        return {"message": "Thank you for your feedback!", "feedback": new_feedback}, 201

    def get(self):
        return {"feedbacks": feedbacks}, 200

api.add_resource(FeedbackListResource, "/feedbacks")

if __name__ == '__main__':
    app.run(debug=True)
