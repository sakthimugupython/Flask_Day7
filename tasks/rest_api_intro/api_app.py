from flask import Flask, jsonify
import time
try:
    from flask_cors import CORS
    cors_available = True
except ImportError:
    cors_available = False

app = Flask(__name__)
if cors_available:
    CORS(app)

start_time = time.time()

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, welcome to the Flask REST API!"}), 200

@app.route('/info', methods=['GET'])
def info():
    return jsonify({
        "app_name": "Flask REST API Demo",
        "version": "1.0.0"
    }), 200

@app.route('/status', methods=['GET'])
def status():
    uptime = round(time.time() - start_time, 2)
    return jsonify({
        "status": "ok",
        "uptime_seconds": uptime
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
