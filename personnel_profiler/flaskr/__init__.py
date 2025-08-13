from flask import Flask
from flask_cors import CORS
from .extensions import db, migrate
from .config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import routes, models
    app.register_blueprint(routes.bp)

    from seed import register_seed_command
    register_seed_command(app)

    return app