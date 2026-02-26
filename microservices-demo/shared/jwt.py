from flask import Flask
from flask_jwt_extended import JWTManager

def init_jwt(app: Flask):
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
    JWTManager(app)