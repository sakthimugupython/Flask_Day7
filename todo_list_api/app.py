from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

tasks = []
task_id_counter = 1

class TaskList(Resource):
    def get(self):
        return {"tasks": tasks}, 200

    def post(self):
        global task_id_counter
        data = request.get_json()
        if not data.get("title"):
            return {"message": "Task title is required."}, 400
        new_task = {
            "id": task_id_counter,
            "title": data["title"],
            "status": data.get("status", False)
        }
        tasks.append(new_task)
        task_id_counter += 1
        return {"message": "Task created successfully", "task": new_task}, 201

class Task(Resource):
    def get(self, id):
        for task in tasks:
            if task["id"] == id:
                return task, 200
        return {"message": "Task not found"}, 404

    def put(self, id):
        data = request.get_json()
        for task in tasks:
            if task["id"] == id:
                # Toggle status if requested
                if "status" in data:
                    task["status"] = data["status"]
                # Update title if provided
                if "title" in data:
                    task["title"] = data["title"]
                return {"message": "Task updated", "task": task}, 200
        return {"message": "Task not found"}, 404

    def delete(self, id):
        for i, task in enumerate(tasks):
            if task["id"] == id:
                tasks.pop(i)
                return {"message": "Task deleted"}, 200
        return {"message": "Task not found"}, 404

api.add_resource(TaskList, "/tasks")
api.add_resource(Task, "/tasks/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
