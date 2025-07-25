from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

cart = []
item_id_counter = 1

class CartListResource(Resource):
    def get(self):
        return {"cart": cart}, 200

    def post(self):
        global item_id_counter
        data = request.get_json()
        if not data.get("product_name") or "quantity" not in data or "price" not in data:
            return {"message": "product_name, quantity, and price are required."}, 400
        try:
            quantity = int(data["quantity"])
            price = float(data["price"])
            if quantity <= 0 or price <= 0:
                return {"message": "Quantity and price must be greater than 0."}, 400
        except (ValueError, TypeError):
            return {"message": "Quantity must be integer and price must be a number."}, 400
        new_item = {
            "id": item_id_counter,
            "product_name": data["product_name"],
            "quantity": quantity,
            "price": price
        }
        cart.append(new_item)
        item_id_counter += 1
        return {"message": "Item added to cart", "item": new_item}, 201

class CartItemResource(Resource):
    def put(self, id):
        data = request.get_json()
        for item in cart:
            if item["id"] == id:
                if "product_name" in data:
                    item["product_name"] = data["product_name"]
                if "quantity" in data:
                    try:
                        quantity = int(data["quantity"])
                        if quantity <= 0:
                            return {"message": "Quantity must be greater than 0."}, 400
                        item["quantity"] = quantity
                    except (ValueError, TypeError):
                        return {"message": "Quantity must be integer."}, 400
                if "price" in data:
                    try:
                        price = float(data["price"])
                        if price <= 0:
                            return {"message": "Price must be greater than 0."}, 400
                        item["price"] = price
                    except (ValueError, TypeError):
                        return {"message": "Price must be a number."}, 400
                return {"message": "Cart item updated", "item": item}, 200
        return {"message": "Item not found"}, 404

    def delete(self, id):
        for i, item in enumerate(cart):
            if item["id"] == id:
                cart.pop(i)
                return {"message": "Item removed from cart"}, 200
        return {"message": "Item not found"}, 404

class CartTotalResource(Resource):
    def get(self):
        total = sum(item["quantity"] * item["price"] for item in cart)
        return {"total_price": total}, 200

api.add_resource(CartListResource, "/cart")
api.add_resource(CartItemResource, "/cart/<int:id>")
api.add_resource(CartTotalResource, "/cart/total")

if __name__ == '__main__':
    app.run(debug=True)
