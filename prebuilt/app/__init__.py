import os
from flask import Flask
from flask_cors import CORS
from .chat_bot import load_chat_model, init_chat_state
from .routes import register_routes

#model = None
#tokenizer = None
#device = None
#state = None

def create_app():
    templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'templates'))
    static_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'static'))


    app = Flask(__name__, template_folder=templates_path, static_folder=static_path)
    CORS(app)

    # Global import
    #global model, tokenizer, device
    #global state
    
    #from .chat_bot import get_device  
    

    #device = get_device()
    #model, tokenizer = load_chat_model(device)  
    
    #state = init_chat_state() # Loads model, TTS, etc
    app.config['state'] = init_chat_state() 

    # Register all routes
    register_routes(app)

    return app