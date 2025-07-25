from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

contacts = []
contact_id_counter = 1

class ContactListResource(Resource):
    def get(self):
        return {"contacts": contacts}, 200

    def post(self):
        global contact_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("phone") or not data.get("email"):
            return {"message": "Name, phone, and email are required."}, 400
        if len(str(data["phone"])) != 10 or not str(data["phone"]).isdigit():
            return {"message": "Phone must be 10 digits."}, 400
        new_contact = {
            "id": contact_id_counter,
            "name": data["name"],
            "phone": str(data["phone"]),
            "email": data["email"]
        }
        contacts.append(new_contact)
        contact_id_counter += 1
        return {"message": "Contact created successfully", "contact": new_contact}, 201

class ContactResource(Resource):
    def get(self, id):
        for contact in contacts:
            if contact["id"] == id:
                return contact, 200
        return {"message": "Contact not found"}, 404

    def put(self, id):
        data = request.get_json()
        for contact in contacts:
            if contact["id"] == id:
                if "name" in data:
                    contact["name"] = data["name"]
                if "phone" in data:
                    if len(str(data["phone"])) != 10 or not str(data["phone"]).isdigit():
                        return {"message": "Phone must be 10 digits."}, 400
                    contact["phone"] = str(data["phone"])
                if "email" in data:
                    contact["email"] = data["email"]
                return {"message": "Contact updated", "contact": contact}, 200
        return {"message": "Contact not found"}, 404

    def delete(self, id):
        for i, contact in enumerate(contacts):
            if contact["id"] == id:
                contacts.pop(i)
                return {"message": "Contact deleted"}, 200
        return {"message": "Contact not found"}, 404

api.add_resource(ContactListResource, "/contacts")
api.add_resource(ContactResource, "/contacts/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
