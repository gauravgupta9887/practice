from flask import Flask
from .config import get_settings
from .api.routes import bp
from .shared.db import init_db

def create_app():
    app = Flask(__name__)
    init_db()
    app.register_blueprint(bp)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=8083)