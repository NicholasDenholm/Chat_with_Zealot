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
            print("Transcription is: ", transcription, "\n")
            chat_state = current_app.config['state']
            #print("Chat state from api_audio:", chat_state)

            if chat_state['backend'] == 'huggingface':
                # Creates or appends the response dictionary, generates ands encodes a new response  
                bot_response = chat_with_speech(transcription, chat_state)  
            
            elif chat_state['backend'] == 'llamacpp':
                current_bot = chat_state['bot_instance']
                history = chat_state['chat_history_ids']
                memory = chat_state['max_memory']
                
                bot_response = current_bot.reply(transcription) 
                print(bot_response)

                # Update the history of responses
                chat_state['chat_history_ids'] = current_bot.modify_chat_history(bot_response, history, memory)

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

        if state['backend'] == 'huggingface':
            response = chat_with_speech(user_input, state)

        elif state['backend'] == 'llamacpp':
            current_bot = state['bot_instance']
            history = state['chat_history_ids']
            memory = state['max_memory']
            
            response = current_bot.reply(user_input) 
            print(response)

            # Update the history of responses
            state['chat_history_ids'] = current_bot.modify_chat_history(response, history, memory)

        else:
            print("Deefault respons handle")
            response = chat_with_speech(user_input, state)


        return jsonify({
            "response": response,
            "chat_history_ids": state['chat_history_ids']
        })

    #TODO make this work with the multi bot setup
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