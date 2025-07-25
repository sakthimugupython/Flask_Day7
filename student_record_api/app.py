from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

students = []
student_id_counter = 1

VALID_GRADES = {"A", "B", "C", "D"}

class StudentListResource(Resource):
    def get(self):
        return {"students": students}, 200

    def post(self):
        global student_id_counter
        data = request.get_json()
        if not data.get("name") or not data.get("roll") or not data.get("grade"):
            return {"message": "Name, roll, and grade are required."}, 400
        if data["grade"] not in VALID_GRADES:
            return {"message": "Grade must be A, B, C, or D only."}, 400
        new_student = {
            "id": student_id_counter,
            "name": data["name"],
            "roll": data["roll"],
            "grade": data["grade"]
        }
        students.append(new_student)
        student_id_counter += 1
        return {"message": "Student created successfully", "student": new_student}, 201

class StudentResource(Resource):
    def put(self, id):
        data = request.get_json()
        for student in students:
            if student["id"] == id:
                if "name" in data:
                    student["name"] = data["name"]
                if "roll" in data:
                    student["roll"] = data["roll"]
                if "grade" in data:
                    if data["grade"] not in VALID_GRADES:
                        return {"message": "Grade must be A, B, C, or D only."}, 400
                    student["grade"] = data["grade"]
                return {"message": "Student updated", "student": student}, 200
        return {"message": "Student not found"}, 404

    def delete(self, id):
        for i, student in enumerate(students):
            if student["id"] == id:
                students.pop(i)
                return {"message": "Student deleted"}, 200
        return {"message": "Student not found"}, 404

api.add_resource(StudentListResource, "/students")
api.add_resource(StudentResource, "/students/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
