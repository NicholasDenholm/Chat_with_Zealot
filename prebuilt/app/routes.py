from flask import request, jsonify, render_template, current_app
import torch
#from . import model, tokenizer, device
#from . import state
from .chat_bot import chat_with_bot
from .chat_bot import chat_with_speech


def register_routes(app):
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


'''
def register_routes(app):

    @app.route('/chat', methods=['POST'])
    def chat():
        data = request.json
        user_input = data.get('message', '')
        chat_history_ids = data.get('chat_history_ids', None)

        if not user_input:
            return jsonify({'error': 'No message provided'}), 400

        if chat_history_ids:
            chat_history_ids = torch.tensor(chat_history_ids).to(device)

        bot_reply, chat_history_ids = chat_with_bot(user_input, tokenizer, model, chat_history_ids, device)

        return jsonify({
            'response': bot_reply,
            'chat_history_ids': chat_history_ids.tolist()
        })

    @app.route('/')
    def home():
        return "Chatbot API is running."

'''