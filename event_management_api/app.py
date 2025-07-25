from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

events = []
event_id_counter = 1

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class EventListResource(Resource):
    def get(self):
        return {"events": events}, 200

    def post(self):
        global event_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("date") or not data.get("location"):
            return {"message": "Name, date, and location are required."}, 400
        if not is_valid_date(data["date"]):
            return {"message": "Date must be in YYYY-MM-DD format."}, 400
        new_event = {
            "id": event_id_counter,
            "name": data["name"],
            "date": data["date"],
            "location": data["location"]
        }
        events.append(new_event)
        event_id_counter += 1
        return {"message": "Event created successfully", "event": new_event}, 201

class EventResource(Resource):
    def get(self, id):
        for event in events:
            if event["id"] == id:
                return event, 200
        return {"message": "Event not found"}, 404

    def put(self, id):
        data = request.get_json()
        for event in events:
            if event["id"] == id:
                if "name" in data:
                    event["name"] = data["name"]
                if "date" in data:
                    if not is_valid_date(data["date"]):
                        return {"message": "Date must be in YYYY-MM-DD format."}, 400
                    event["date"] = data["date"]
                if "location" in data:
                    event["location"] = data["location"]
                return {"message": "Event updated", "event": event}, 200
        return {"message": "Event not found"}, 404

    def delete(self, id):
        for i, event in enumerate(events):
            if event["id"] == id:
                events.pop(i)
                return {"message": "Event deleted"}, 200
        return {"message": "Event not found"}, 404

api.add_resource(EventListResource, "/events")
api.add_resource(EventResource, "/events/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
