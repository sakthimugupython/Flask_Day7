from flask import jsonify

def ApiResponse(data=None, message=None, error=None, status=200):
    resp = {"success": error is None}
    if data is not None:
        resp["data"] = data
    if message:
        resp["message"] = message
    if error:
        resp["error"] = error
    return jsonify(resp), status
