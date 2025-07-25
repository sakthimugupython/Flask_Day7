from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []
item_id_counter = 1
THRESHOLD = 5

class ItemListResource(Resource):
    def get(self):
        return {"items": items}, 200

    def post(self):
        global item_id_counter
        data = request.get_json()
        if not data.get("item_name") or "quantity" not in data or not data.get("category"):
            return {"message": "item_name, quantity, and category are required."}, 400
        try:
            quantity = int(data["quantity"])
        except (ValueError, TypeError):
            return {"message": "Quantity must be an integer."}, 400
        new_item = {
            "id": item_id_counter,
            "item_name": data["item_name"],
            "quantity": quantity,
            "category": data["category"]
        }
        items.append(new_item)
        item_id_counter += 1
        return {"message": "Item added to inventory", "item": new_item}, 201

class ItemResource(Resource):
    def put(self, id):
        data = request.get_json()
        for item in items:
            if item["id"] == id:
                if "item_name" in data:
                    item["item_name"] = data["item_name"]
                if "quantity" in data:
                    try:
                        quantity = int(data["quantity"])
                        item["quantity"] = quantity
                        if quantity < THRESHOLD:
                            item["warning"] = "Quantity below threshold!"
                        else:
                            item.pop("warning", None)
                    except (ValueError, TypeError):
                        return {"message": "Quantity must be an integer."}, 400
                if "category" in data:
                    item["category"] = data["category"]
                return {"message": "Item updated", "item": item}, 200
        return {"message": "Item not found"}, 404

    def delete(self, id):
        for i, item in enumerate(items):
            if item["id"] == id:
                items.pop(i)
                return {"message": "Item deleted"}, 200
        return {"message": "Item not found"}, 404

api.add_resource(ItemListResource, "/items")
api.add_resource(ItemResource, "/items/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
