from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

results = []
result_id_counter = 1

def calculate_grade(avg):
    if avg >= 90:
        return "A"
    elif avg >= 75:
        return "B"
    elif avg >= 60:
        return "C"
    else:
        return "D"

class ResultListResource(Resource):
    def get(self):
        return {"results": results}, 200

    def post(self):
        global result_id_counter
        data = request.get_json()
        try:
            maths = float(data["maths"])
            science = float(data["science"])
            english = float(data["english"])
        except (KeyError, ValueError, TypeError):
            return {"message": "maths, science, and english are required and must be numbers."}, 400
        if not data.get("name"):
            return {"message": "name is required."}, 400
        avg = (maths + science + english) / 3
        grade = calculate_grade(avg)
        new_result = {
            "id": result_id_counter,
            "name": data["name"],
            "maths": maths,
            "science": science,
            "english": english,
            "average": avg,
            "grade": grade
        }
        results.append(new_result)
        result_id_counter += 1
        return {"message": "Result added successfully", "result": new_result}, 201

class ResultResource(Resource):
    def put(self, id):
        data = request.get_json()
        for result in results:
            if result["id"] == id:
                try:
                    if "maths" in data:
                        result["maths"] = float(data["maths"])
                    if "science" in data:
                        result["science"] = float(data["science"])
                    if "english" in data:
                        result["english"] = float(data["english"])
                except (ValueError, TypeError):
                    return {"message": "Marks must be numbers."}, 400
                if "name" in data:
                    result["name"] = data["name"]
                avg = (result["maths"] + result["science"] + result["english"]) / 3
                result["average"] = avg
                result["grade"] = calculate_grade(avg)
                return {"message": "Result updated", "result": result}, 200
        return {"message": "Result not found"}, 404

api.add_resource(ResultListResource, "/results")
api.add_resource(ResultResource, "/results/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
