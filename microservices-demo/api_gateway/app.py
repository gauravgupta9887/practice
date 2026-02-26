from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
import requests

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret-key"

jwt = JWTManager(app)

def forward():
    path = request.full_path
    method = request.method
    headers = dict(request.headers)
    data = request.get_json(force=True, silent=True)
    # replace host with the microservice that owns the prefix
    if request.path.startswith("/api/users"):
        target = "http://user_service:8081" + request.path
    elif request.path.startswith("/api/inventory"):
        target = "http://inventory_service:8082" + request.path
    elif request.path.startswith("/api/order"):
        target = "http://order_service:8083" + request.path
    else:
        return jsonify({"msg":"unknown endpoint"}), 404

    r = requests.request(method, target, headers=headers, json=data, timeout=5)
    return (r.content, r.status_code, r.headers.items())

app.add_url_rule("/", defaults={"path": ""}, view_func=forward, methods=["GET"])
app.add_url_rule("/<path:path>", view_func=forward)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)