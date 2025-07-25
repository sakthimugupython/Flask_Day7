from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

workouts = []
workout_id_counter = 1

class WorkoutListResource(Resource):
    def get(self):
        return {"workouts": workouts}, 200

    def post(self):
        global workout_id_counter
        data = request.get_json()
        if not data.get("user") or not data.get("type") or "duration" not in data:
            return {"message": "User, type, and duration are required."}, 400
        try:
            duration = float(data["duration"])
            if duration <= 0:
                return {"message": "Duration must be greater than 0."}, 400
        except (ValueError, TypeError):
            return {"message": "Duration must be a number."}, 400
        new_workout = {
            "id": workout_id_counter,
            "user": data["user"],
            "type": data["type"],
            "duration": duration
        }
        workouts.append(new_workout)
        workout_id_counter += 1
        return {"message": "Workout logged successfully", "workout": new_workout}, 201

class WorkoutResource(Resource):
    def get(self, id):
        for workout in workouts:
            if workout["id"] == id:
                return workout, 200
        return {"message": "Workout not found"}, 404

    def put(self, id):
        data = request.get_json()
        for workout in workouts:
            if workout["id"] == id:
                if "user" in data:
                    workout["user"] = data["user"]
                if "type" in data:
                    workout["type"] = data["type"]
                if "duration" in data:
                    try:
                        duration = float(data["duration"])
                        if duration <= 0:
                            return {"message": "Duration must be greater than 0."}, 400
                        workout["duration"] = duration
                    except (ValueError, TypeError):
                        return {"message": "Duration must be a number."}, 400
                return {"message": "Workout updated", "workout": workout}, 200
        return {"message": "Workout not found"}, 404

    def delete(self, id):
        for i, workout in enumerate(workouts):
            if workout["id"] == id:
                workouts.pop(i)
                return {"message": "Workout deleted"}, 200
        return {"message": "Workout not found"}, 404

class WorkoutSummaryResource(Resource):
    def get(self):
        total_duration = sum(w["duration"] for w in workouts)
        return {"total_duration": total_duration}, 200

api.add_resource(WorkoutListResource, "/workouts")
api.add_resource(WorkoutResource, "/workouts/<int:id>")
api.add_resource(WorkoutSummaryResource, "/workouts/summary")

if __name__ == '__main__':
    app.run(debug=True)
