from flask import request, jsonify, render_template, current_app
from prebuilt.app.chat_bot import chat_with_speech
from prebuilt.app.audio_bot import Whisper_Bot
import tempfile
import os

#from bots import whisper_bot

### a route is how the app knows what code to run when a user accesses a certain URL.

def register_routes(app): # regester_routes called with __init__, keeps chat and home modular
    
    whisper_bot = Whisper_Bot(model_name="base")

    @app.route('/api/audio', methods=["POST"])
    def api_audio():
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file provided"}), 400

        audio_file = request.files['audio']

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp:
            audio_path = temp.name
            audio_file.save(audio_path)

        try:
            transcription = whisper_bot.transcribe_audio(audio_path)
            chat_state = current_app.config['state']
            
            bot_response = chat_with_speech(transcription, chat_state)

            return jsonify({
                "transcription": transcription,
                "response": bot_response
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            os.remove(audio_path)


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

    @app.route("/run_conversation", methods=["POST"])
    def run_conversation():
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