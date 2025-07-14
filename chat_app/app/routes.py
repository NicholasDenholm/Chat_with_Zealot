from flask import request, jsonify, render_template, current_app
from prebuilt.app.chat_bot import chat_with_speech, chat_with_speech_string_version
from prebuilt.app.audio_bot import Whisper_Bot
from .bot import get_current_bot_info, swap_bot, init_bot


#swap_bot, get_current_bot_info, init_bot
import tempfile
import os

# Page configuration presets
PAGE_CONFIGS = {
    'chat_bot': {
        'pages': [
            {'key': 'home', 'label': 'Home', 'url': '/', 'paths': ['', 'home']},
            {'key': 'bot-selector', 'label': 'Bot Selector', 'url': '/bot-menu', 'paths': ['bot-menu', 'bot-selector']},
        ]
    },
    'home': {
        'pages': [
            {'key': 'home', 'label': 'Chat', 'url': '/talk-to-bot', 'paths': ['talk-to-bot', 'chat']},
            {'key': 'bot-selector', 'label': 'Bot Selector', 'url': '/bot-menu', 'paths': ['bot-menu', 'bot-selector']},
        ]
    },
    'bot_menu': {
        'pages': [
            {'key': 'home', 'label': 'Home', 'url': '/', 'paths': ['', 'home']},
            {'key': 'home', 'label': 'Chat', 'url': '/talk-to-bot', 'paths': ['talk-to-bot', 'chat']},
            {'key': 'bot-selector', 'label': 'Bot Selector', 'url': '/bot-menu', 'paths': ['bot-menu', 'bot-selector']},
        ]
    }
}

def get_page_switcher_config(config_name='chat_bot', position='top-left'):
    """Generate page switcher configuration for templates"""
    config = PAGE_CONFIGS.get(config_name, PAGE_CONFIGS['chat_bot'])
    current_path = request.path
    
    # Mark active page
    pages = []
    js_config = {}
    
    for page in config['pages']:
        page_copy = page.copy()
        page_copy['active'] = any(path in current_path for path in page['paths'])
        pages.append(page_copy)
        
        # Build JavaScript configuration
        js_config[page['key']] = {
            'url': page['url'],
            'paths': page['paths']
        }
    
    return {
        'pages': pages,
        'position': position,
        'config_name': config_name,
        'switcher_js_config': js_config  # This is for the JavaScript
    }
### a route is how the app knows what code to run when a user accesses a certain URL.

def register_routes(app): # regester_routes called with __init__, keeps chat and home modular
    
    # ----------------- Chatting  ----------------- #
    
    #TODO Make it so that the whisper bot can be swapped out to another language
    whisper_bot = Whisper_Bot(model_name="base")

    def generate_response(user_input, chat_state):
        """Common logic for generating bot responses"""

        if chat_state['backend'] == 'huggingface':
            response = chat_with_speech(user_input, chat_state)
            chat_state['chat_history_ids'] = chat_state['chat_history_string']
        
        elif chat_state['backend'] == 'llamacpp':
            current_bot = chat_state['bot_instance']
            history = chat_state['chat_history_ids']
            memory = chat_state['max_memory']

            if history is None:
                history = []
                chat_state['chat_history_ids'] = history            

            current_bot.add_user_message(user_input, history, memory)   # Add user message to history

            response = current_bot.reply(user_input, chat_history=history)  # reply with context

            current_bot.add_bot_message(response, history, memory)  # Add bot response to history
        
        else:
            print("Default response handle")
            response = chat_with_speech(user_input, chat_state)

        return response


    def make_new_bot(current_app, backend, model):
        try:
            
            if not backend or not model:
                print("ERROR: NO BACKEND OR MODEL", backend, model)
                return jsonify({'error': 'backend and model are required'}), 400
            
            print("\nbefore init_bot in routes make_new_bot", backend, model)
            init_bot(current_app, backend, model)
            print("here")
            #print(app['backend'])
            #app = create_app(backend=model, model=model)
            print("After init_bot in routes make_new_bot", backend, model, "\n")
            
            return jsonify({
                'success': True,
                'backend': backend,
                'model': model,
                'message': 'Bot initialized successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

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

            bot_response = generate_response(transcription, chat_state)
            print(bot_response)

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

        print("Chat data is: ",data, "\n\n\n")

        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        state = current_app.config['state']
        print("Current state now: ",state, "\n")

        response = generate_response(user_input, state)
        print('Response from routes function, chat() is: ',response)

        # TODO ERROR HERE for the bot swap then talk, response is good, chat_history_ids is not.
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

    # ----------------- Changing Bots ----------------- # 
    @app.route('/api/bot/swap', methods=['POST'])
    def api_swap_bot():
        try:
            data = request.json
            backend = data.get('backend')
            model = data.get('model')
            
            if not backend or not model:
                return jsonify({'error': 'backend and model are required'}), 400
            
            result = swap_bot(current_app, backend, model)
            print('result from swap bot:', result , "\n\n")
            #print(result['state'])
            #app = current_app
            #if (result['success']):
                #backend = result['backend']
                #model = result['model']

                #result = make_new_bot(current_app, backend, model)
                #current_app = create_app(backend=model, model=model)

            return jsonify({
                'success': result['success'],
                'backend': result['backend'],
                'model': result['model'],
                'message': 'Bot initialized successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/bot/current', methods=['GET'])
    def api_get_current_bot():
        try:
            info = get_current_bot_info(current_app)
            print("current bot info:", info)

            #data = request.json
            #backend = data.get('backend')
            #model = data.get('model')
            #print("backend: ", backend, "and model: ", model)

            return jsonify(info)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/bot/init', methods=['POST'])
    def api_init_bot():
        try:
            data = request.json
            backend = data.get('backend')
            model = data.get('model')
            
            if not backend or not model:
                return jsonify({'error': 'backend and model are required'}), 400
            
            print("\nbefore init_bot in routes api_init_bot", backend, model)
            init_bot(current_app, backend, model)
            print("After init_bot in routes api_init_bot", backend, model, "\n")
            
            return jsonify({
                'success': True,
                'backend': backend,
                'model': model,
                'message': 'Bot initialized successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    # ----------------- Pages ----------------- # 
    @app.route("/")
    def home():
        #return "Chatbot API is running."
        switcher_config = get_page_switcher_config('home', 'top-left')
        print("Switcher config:", switcher_config)
        return render_template("navigation.html")
    
    @app.route("/talk-to-bot")
    def talk_to_bot():
        switcher_config = get_page_switcher_config('chat_bot', 'top-left')
        print("Switcher config:", switcher_config)
        
        return render_template("talk_to_bot.html", switcher=switcher_config)
    
    @app.route('/bot-menu')
    def bot_menu():
        switcher_config = get_page_switcher_config('bot_menu', 'top-left')
        print("Switcher config:", switcher_config)
        return render_template('bot_menu.html')