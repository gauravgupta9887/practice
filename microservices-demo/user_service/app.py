from flask import Flask
from .config import get_settings
from .api.routes import bp
from .shared.db import init_db
from .shared.jwt import init_jwt

def create_app():
    app = Flask(__name__)
    settings = get_settings()
    app.config["PORT"] = settings.port

    init_jwt(app)
    init_db()

    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=app.config["PORT"])