from flask import request, jsonify, render_template, current_app
#import torch
#from .chat_bot import chat_with_bot
from .chat_bot import chat_with_speech

### a route is how the app knows what code to run when a user accesses a certain URL.

def register_routes(app): # regester_routes called with __init__, keeps chat and home modular
    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json
        user_input = data.get("message", "")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        state = current_app.config['state']
        response = chat_with_speech(user_input, state)

        return jsonify({
            "response": response,
            "chat_history_ids": state['chat_history_ids'].tolist()
        })

    @app.route("/")
    def home():
        #return "Chatbot API is running."
        return render_template("index.html")