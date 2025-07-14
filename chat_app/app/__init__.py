import os
from flask import Flask
from flask_cors import CORS
from .bot import init_model_state, init_bot
from .routes import register_routes

def create_app(backend:str=None, model:str=None):
    # retrive html/css/js scripts from static and templates folder
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'templates'))
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    CORS(app)

    # Initialize bot if parameters provided
    if backend and model:
        init_bot(app, backend, model)

    # Register all routes
    register_routes(app)

    return app
