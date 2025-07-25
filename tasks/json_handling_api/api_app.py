from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/echo', methods=['POST'])
def echo():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Invalid or missing JSON body."}), 400
    # Print incoming data
    print("Received JSON:", data)
    return jsonify({"received": data}), 200

@app.route('/profile_bio', methods=['POST'])
def profile_bio():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Missing JSON body."}), 400
    bio = data.get('profile', {}).get('bio')
    return jsonify({"bio": bio}), 200

@app.route('/multiply', methods=['POST'])
def multiply():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 400
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Missing or invalid JSON body."}), 400
    a = data.get('a')
    b = data.get('b')
    if type(a) not in [int, float] or type(b) not in [int, float]:
        return jsonify({"error": "Both a and b must be numbers."}), 400
    return jsonify({"product": a * b}), 200

@app.route('/json_loads', methods=['POST'])
def json_loads_route():
    try:
        raw = request.data.decode('utf-8')
        parsed = json.loads(raw)
    except Exception as e:
        return jsonify({"error": f"Invalid JSON: {str(e)}"}), 400
    return jsonify({"parsed": parsed}), 200

@app.route('/explain', methods=['GET'])
def explain():
    return jsonify({
        "raw": "Raw: Send JSON as plain text (Content-Type: application/json)",
        "form-data": "Form-data: Key-value pairs, can include files (Content-Type: multipart/form-data)",
        "x-www-form-urlencoded": "URL-encoded: Key-value pairs in URL encoding (Content-Type: application/x-www-form-urlencoded)"
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
