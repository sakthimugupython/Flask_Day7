from flask import Flask, jsonify, request

app = Flask(__name__)

users = []
user_id_counter = 1

def get_user_by_id(uid):
    for user in users:
        if user["id"] == uid:
            return user
    return None

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({"users": users}), 200

@app.route('/api/users', methods=['POST'])
def add_user():
    global user_id_counter
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Missing JSON body."}), 400
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return jsonify({"error": "Name and email are required."}), 400
    if any(u["email"] == email for u in users):
        return jsonify({"error": "Email already exists."}), 400
    new_user = {"id": user_id_counter, "name": name, "email": email}
    users.append(new_user)
    user_id_counter += 1
    return jsonify({"message": "User created", "user": new_user}), 201

@app.route('/api/users/<int:uid>', methods=['GET'])
def get_user(uid):
    user = get_user_by_id(uid)
    if user:
        return jsonify(user), 200
    return jsonify({"error": "User not found."}), 404

@app.route('/api/users/<int:uid>', methods=['PUT'])
def update_user(uid):
    data = request.get_json(force=True, silent=True)
    if not data:
        return jsonify({"error": "Missing JSON body."}), 400
    user = get_user_by_id(uid)
    if not user:
        return jsonify({"error": "User not found."}), 404
    name = data.get("name", user["name"])
    email = data.get("email", user["email"])
    if email != user["email"] and any(u["email"] == email for u in users):
        return jsonify({"error": "Email already exists."}), 400
    user["name"] = name
    user["email"] = email
    return jsonify({"message": "User updated", "user": user}), 200

@app.route('/api/users/<int:uid>', methods=['DELETE'])
def delete_user(uid):
    global users
    user = get_user_by_id(uid)
    if not user:
        return jsonify({"error": "User not found."}), 404
    users = [u for u in users if u["id"] != uid]
    return jsonify({"message": "User deleted"}), 200

@app.route('/api/users/clear', methods=['DELETE'])
def clear_users():
    global users, user_id_counter
    users = []
    user_id_counter = 1
    return jsonify({"message": "All users cleared."}), 200

if __name__ == '__main__':
    app.run(debug=True)
