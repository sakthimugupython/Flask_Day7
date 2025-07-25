from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

issues = []
issue_id_counter = 1
VALID_STATUS = {"open", "closed"}

class IssueListResource(Resource):
    def get(self):
        return {"issues": issues}, 200

    def post(self):
        global issue_id_counter
        data = request.get_json()
        if not data.get("title") or not data.get("description") or not data.get("status"):
            return {"message": "title, description, and status are required."}, 400
        if data["status"] not in VALID_STATUS:
            return {"message": "Status must be 'open' or 'closed'."}, 400
        new_issue = {
            "id": issue_id_counter,
            "title": data["title"],
            "description": data["description"],
            "status": data["status"]
        }
        issues.append(new_issue)
        issue_id_counter += 1
        return {"message": "Issue reported successfully", "issue": new_issue}, 201

class IssueResource(Resource):
    def put(self, id):
        data = request.get_json()
        for issue in issues:
            if issue["id"] == id:
                if "title" in data:
                    issue["title"] = data["title"]
                if "description" in data:
                    issue["description"] = data["description"]
                if "status" in data:
                    if data["status"] not in VALID_STATUS:
                        return {"message": "Status must be 'open' or 'closed'."}, 400
                    issue["status"] = data["status"]
                return {"message": "Issue updated", "issue": issue}, 200
        return {"message": "Issue not found"}, 404

    def delete(self, id):
        for i, issue in enumerate(issues):
            if issue["id"] == id:
                issues.pop(i)
                return {"message": "Issue deleted"}, 200
        return {"message": "Issue not found"}, 404

api.add_resource(IssueListResource, "/issues")
api.add_resource(IssueResource, "/issues/<int:id>")

if __name__ == '__main__':
    app.run(debug=True)
