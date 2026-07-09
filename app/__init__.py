from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.config import Config


db = SQLAlchemy()


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    from .models import Contribution, Group, Member, Payout, User
    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app
