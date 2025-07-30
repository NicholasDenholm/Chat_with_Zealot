from flask import request, jsonify, render_template, current_app
from prebuilt.app.chat_bot import chat_with_speech, chat_with_speech_string_version
from prebuilt.app.audio_bot import Whisper_Bot
#from bots.whisper_bot import Whisper_Bot
from .bot import get_current_bot_info, swap_bot, init_bot, swap_personality

import tempfile
import os

# Page configuration presets
'''
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
'''

whisper_bot = Whisper_Bot(model_name="base")
#whisper_bot.set_language('en')

### a route is how the app knows what code to run when a user accesses a certain URL.
def register_routes(app):
    
    whisper_bot = Whisper_Bot(model_name="base")
    
    @app.route("/set_language", methods=["POST"])
    def set_language():
        data = request.json
        lang = data.get("language_code")
        print("language code is: ", lang)
        #print(isinstance(lang, str))

        if not lang:
            return jsonify({"error": "No language code provided"}), 400
        #whisper_bot = Whisper_Bot(model_name="medium")
        whisper_bot.set_language(lang)
        return jsonify({"message": f"Language set to {lang}."})
        
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
            language = whisper_bot.language_code
            print("Language used here: ", language)
            transcription = whisper_bot.transcribe_audio(audio_path, True)
            print("transcription: ", transcription)
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

    # ----------------- Chatting  ----------------- #
    
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

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.json

        #print("Chat data is: ",data, "\n\n\n")

        user_input = data.get("message", "")
        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        state = current_app.config['state']
        #print("Current state now: ",state, "\n")

        response = generate_response(user_input, state)
        #print('Response from routes function, chat() is: ',response)

        # Note, if response above is good, check if chat_history_ids is in string form.
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
    
    # TODO check if this method is used 
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

    
    @app.route('/api/bot/swap', methods=['POST'])
    def api_swap_bot(): 
        try:
            data = request.json
            backend = data.get('backend')
            model = data.get('model')
            botType = data.get('botType')
            
            if not backend or not model:
                return jsonify({'error': 'backend and model are required'}), 400
            
            result = swap_bot(current_app, backend, model, botType)
            #print('result from swap bot:', result , "\n\n")

            return jsonify({
                'success': result['success'],
                'backend': result['backend'],
                'model': result['model'],
                'botType': result['botType'],
                'message': 'Bot initialized successfully'
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500


    @app.route('/api/bot/current', methods=['GET'])
    def api_get_current_bot():
        try:
            info = get_current_bot_info(current_app)
            print("current bot info:", info)
            return jsonify(info)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    '''
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
    '''

    # ----------------- Changing Personalities ----------------- #

    @app.route('/api/bot/personality_change', methods=['POST'])
    def api_personality_change():
        try:
            data = request.json
            backend = data.get('backend')
            personality = data.get('personality')
            #print("data here: ", data)
            #bot_instance = data.get('bot_instance')

            if not backend or not personality:
                return jsonify({'error': 'backend and personality are required'}), 400

            result = swap_personality(current_app, backend, personality)
            #print("result after personality swap : ", result, "\n")

            return jsonify({
                'success': result['success'],
                'backend': result['backend'],
                'personality': result['state']['personality'],
                'message': 'Bots personality changed successfully'
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    # ----------------- Conditional Page Switching ----------------- # 
    @app.route('/api/page/switch', methods=['POST'])
    def switch_page():
        try:
            data = request.json
            page = data.get('page')
            backend = data.get('backend')
             
            if backend == 'llamacpp':
                return jsonify({
                    'success': True,
                    'redirect_url': '/llamacpp',  # Your llamacpp page route
                    'message': 'Switching to LlamaCPP interface'
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Invalid backend for page switch'
                })
                
        except Exception as e:
            return jsonify({
                'success': False,
                'error': str(e)
            })

    # ----------------- Pages ----------------- # 
    @app.route("/")
    def home():
        return render_template("navigation.html")
    
    @app.route("/talk-to-bot")
    def talk_to_bot():
        return render_template("talk_to_bot.html")
    
    @app.route('/bot-menu')
    def bot_menu():
        return render_template('bot_menu.html')
    
    # Personality menus
    @app.route('/personality-menu-assistant')
    def personality_menu_assistant():
        return render_template('personality_menu_assistant.html')
    
    @app.route('/personality-menu-coder')
    def personality_menu_coder():
        return render_template('personality_menu_coder.html')
    
    @app.route('/personality-menu-zealot')
    def personality_menu_zealot():
        return render_template('personality_menu_zealot.html')