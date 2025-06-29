import os
from flask import Flask
from flask_cors import CORS
from .bot import init_model_state
from .routes import register_routes

def create_app(backend:str, model:str):
    # retrive html/css/js scripts from static and templates folder
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'templates'))
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))

    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    CORS(app)

    app.config['state'] = init_model_state(backend, model) 

    # Register all routes
    register_routes(app)

    return app