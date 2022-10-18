import os

from flask import Flask
from flask_login import LoginManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from . import db
    db.init_db(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)
    auth.init_login(login_manager)

    @app.route('/')
    def index():
        return '<h1>index</h1><p><a href="/auth/login">Login</a><p><a href="/auth/logout">Logout</a>'

    return app
