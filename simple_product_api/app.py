from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

products = []
product_id_counter = 1

class ProductListResource(Resource):
    def get(self):
        return {"products": products}, 200

    def post(self):
        global product_id_counter
        data = request.get_json()
        if not data.get("name") or "price" not in data or "in_stock" not in data:
            return {"message": "Name, price, and in_stock are required."}, 400
        try:
            price = float(data["price"])
            if price <= 0:
                return {"message": "Price must be greater than 0."}, 400
        except (ValueError, TypeError):
            return {"message": "Price must be a valid number."}, 400
        new_product = {
            "id": product_id_counter,
            "name": data["name"],
            "price": price,
            "in_stock": bool(data["in_stock"])
        }
        products.append(new_product)
        product_id_counter += 1
        return {"message": "Product created successfully", "product": new_product}, 201

class ProductResource(Resource):
    def get(self, id):
        for product in products:
            if product["id"] == id:
                return product, 200
        return {"message": "Product not found"}, 404

    def put(self, id):
        data = request.get_json()
        for product in products:
            if product["id"] == id:
                if "name" in data:
                    product["name"] = data["name"]
                if "price" in data:
                    try:
                        price = float(data["price"])
                        if price <= 0:
                            return {"message": "Price must be greater than 0."}, 400
                        product["price"] = price
                    except (ValueError, TypeError):
                        return {"message": "Price must be a valid number."}, 400
                if "in_stock" in data:
                    product["in_stock"] = bool(data["in_stock"])
                return {"message": "Product updated", "product": product}, 200
        return {"message": "Product not found"}, 404

    def delete(self, id):
        for i, product in enumerate(products):
            if product["id"] == id:
                products.pop(i)
                return {"message": "Product deleted"}, 200
        return {"message": "Product not found"}, 404

api.add_resource(ProductListResource, "/products")
api.add_resource(ProductResource, "/products/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
