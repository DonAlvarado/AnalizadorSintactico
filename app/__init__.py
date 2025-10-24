# app/__init__.py
from flask import Flask
from flask_cors import CORS
from . import routes
import os

def create_app():
    template_folder = os.path.join(os.path.dirname(__file__), "Front", "templates")
    static_folder = os.path.join(os.path.dirname(__file__), "Front", "static")

    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
    CORS(app)

    app.register_blueprint(routes.bp)
    app.register_blueprint(routes.bp2)

    return app
