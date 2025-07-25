from flask import Flask, request
from flask_restful import Resource, Api
from datetime import datetime

app = Flask(__name__)
api = Api(app)

appointments = []
appointment_id_counter = 1

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

class AppointmentListResource(Resource):
    def get(self):
        return {"appointments": appointments}, 200

    def post(self):
        global appointment_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("date") or not data.get("service"):
            return {"message": "Name, date, and service are required."}, 400
        if not is_valid_date(data["date"]):
            return {"message": "Date must be in YYYY-MM-DD format."}, 400
        new_appointment = {
            "id": appointment_id_counter,
            "name": data["name"],
            "date": data["date"],
            "service": data["service"]
        }
        appointments.append(new_appointment)
        appointment_id_counter += 1
        return {"message": "Appointment booked successfully", "appointment": new_appointment}, 201

class AppointmentResource(Resource):
    def put(self, id):
        data = request.get_json()
        for appointment in appointments:
            if appointment["id"] == id:
                if "name" in data:
                    appointment["name"] = data["name"]
                if "date" in data:
                    if not is_valid_date(data["date"]):
                        return {"message": "Date must be in YYYY-MM-DD format."}, 400
                    appointment["date"] = data["date"]
                if "service" in data:
                    appointment["service"] = data["service"]
                return {"message": "Appointment updated", "appointment": appointment}, 200
        return {"message": "Appointment not found"}, 404

    def delete(self, id):
        for i, appointment in enumerate(appointments):
            if appointment["id"] == id:
                appointments.pop(i)
                return {"message": "Appointment cancelled"}, 200
        return {"message": "Appointment not found"}, 404

api.add_resource(AppointmentListResource, "/appointments")
api.add_resource(AppointmentResource, "/appointments/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
