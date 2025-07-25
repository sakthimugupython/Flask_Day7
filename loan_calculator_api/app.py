from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class LoanCalculatorResource(Resource):
    def post(self):
        data = request.get_json()
        try:
            amount = float(data["amount"])
            interest = float(data["interest"])
            years = int(data["years"])
        except (KeyError, ValueError, TypeError):
            return {"message": "amount, interest, and years are required and must be numeric."}, 400
        if amount <= 0 or interest <= 0 or years <= 0:
            return {"message": "All fields must be positive."}, 400
        r = interest / (12 * 100)
        n = years * 12
        emi = (amount * r * (1 + r) ** n) / ((1 + r) ** n - 1)
        return {"emi": round(emi, 2)}, 200

api.add_resource(LoanCalculatorResource, "/loan/calculate")

if __name__ == '__main__':
    app.run(debug=True)
