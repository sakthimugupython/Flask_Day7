from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tickets = []
ticket_id_counter = 1

class TicketListResource(Resource):
    def get(self):
        return {"tickets": tickets}, 200

    def post(self):
        global ticket_id_counter
        data = request.get_json()
        if not data.get("email") or not data.get("issue") or not data.get("priority"):
            return {"message": "Email, issue, and priority are required."}, 400
        new_ticket = {
            "id": ticket_id_counter,
            "email": data["email"],
            "issue": data["issue"],
            "priority": data["priority"],
            "resolved": False
        }
        tickets.append(new_ticket)
        ticket_id_counter += 1
        return {"message": "Ticket submitted successfully", "ticket": new_ticket}, 201

class TicketResource(Resource):
    def put(self, id):
        data = request.get_json()
        for ticket in tickets:
            if ticket["id"] == id:
                if "resolved" in data and data["resolved"]:
                    ticket["resolved"] = True
                    return {"message": "Ticket closed", "ticket": ticket}, 200
                # Allow updating issue/priority as well
                if "issue" in data:
                    ticket["issue"] = data["issue"]
                if "priority" in data:
                    ticket["priority"] = data["priority"]
                return {"message": "Ticket updated", "ticket": ticket}, 200
        return {"message": "Ticket not found"}, 404

    def delete(self, id):
        for i, ticket in enumerate(tickets):
            if ticket["id"] == id:
                tickets.pop(i)
                return {"message": "Ticket deleted"}, 200
        return {"message": "Ticket not found"}, 404

api.add_resource(TicketListResource, "/tickets")
api.add_resource(TicketResource, "/tickets/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
