import os
import sqlite3
from flask import Flask, g, session, redirect, url_for, request
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    @app.before_request
    def require_login():
        allowed_routes = {"main.login", "static"}
        if request.endpoint not in allowed_routes and "user_id" not in session:
            return redirect(url_for("main.login"))

    def get_db():
        if "db" not in g:
            g.db = sqlite3.connect(
                app.config["DATABASE_PATH"],
                detect_types=sqlite3.PARSE_DECLTYPES
            )
            g.db.row_factory = sqlite3.Row
            g.db.execute("PRAGMA foreign_keys = ON")
        return g.db

    @app.teardown_appcontext
    def close_db(e=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    from app import routes
    app.register_blueprint(routes.bp)

    from app import vulnerable_search
    app.register_blueprint(vulnerable_search.bp)

    return app