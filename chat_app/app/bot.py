import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from prebuilt.app.chat_bot import init_chat_state
import bots

def init_model_state(backend: str = 'huggingface', model_name: str = None, personality: str = None):
    '''
    Creates model with either huggingface or llamacpp backends.
    Args: backend , model_name, device
    '''
    print("\n ---- init_model_state ---- ")
    print("Backend:", backend, "Model name: ", model_name, "\n")

    # x set up dumb bot
    if backend == "huggingface":
        state = init_chat_state()
        #print("Type of state:", type(state))
        #print("State value:", state, "\n")
        return state
    
    # x set up zealot bot
    elif backend == "llamacpp":
        
        if personality is None:
            # Default bot creation.
            bot = bots.build_smart_bot(model_name, 'short_answers')
            #bot = bots.build_zealot_bot(model_name, 'fanatic')
            #bot = bots.build_zealot_bot(model_name, 'short_answers')
            #bot = bots.build_smart_bot(model_name, 'nice_person')
            #bot = bots.build_coding_bot(model_name, 'expert_coder')
        else:
            bot = bots.build_smart_bot(model_name, personality=personality)

        
        max_memory = 10
        
        state = create_ollama_bot_dict(bot.model_name, bot, backend, max_memory)
        print("\n Ollama bot here: ", state, "\n")

        return state
    else: 
        raise ValueError(f"Unsupported backend: {backend}")
    
    
    
    # TODO setup general smart/dumb bots
    # TODO setup multimodal bot
    '''
    elif backend == "openai":
        model_name = model_name or "gpt-4"
        # No need for tokenizer/model loading
        return {
            "backend": backend,
            "model_name": model_name,
            "api_key": os.getenv("OPENAI_API_KEY"),
            "tts_engine": tts_engine,
        }

    '''
    


def init_bot(app, backend: str, model: str):
    """Initialize the bot model state for the app"""
    print("Making new bot with a backend of: ", backend, "and a name of: ", model)
    app.config['state'] = init_model_state(backend, model)
    #print("\n\n============","model state","============\n\n", app.config['state'], "\n============\n\n")

    app.config['current_backend'] = backend
    app.config['current_model'] = model


### -------------- Changing Bots -------------- ###

def swap_bot(app, backend: str, model: str):
    """Swap out the current bot with a new one"""
    # Clean up existing state if needed
    if 'state' in app.config and hasattr(app.config['state'], 'cleanup'):
        app.config['state'].cleanup()

    #print("\n\n--------- before swap_bot in bot.py ---------", backend, model)
    # Initialize new bot
    init_bot(app, backend, model)
    #print("--------- After swap_bot in bot.py", backend, model, "---------\n\n")
    #print("model state at the end of swap_bot:", app.config.get('state'), '\n\n')
    
    return {
        'success': True,
        'backend': backend,
        'model': model,
        'previous_backend': app.config.get('current_backend'),
        'previous_model': app.config.get('current_model'),
        'state': app.config.get('state')
    }

def get_current_bot_info(app):
    """Get information about the currently active bot"""
    state = app.config.get('state')
    personality = state.get('personality') if state else None

    return {
        'backend': app.config.get('current_backend'),
        'model': app.config.get('current_model'),
        'personality': personality,
        'initialized': 'state' in app.config and app.config['state'] is not None
    }


### -------------- Changing Personalities -------------- ###

def swap_personality(app, backend: str, personality: str):
    # Check to make sure its a ollama type bot
    if backend != "llamacpp":
        print("fails at backend check in change_personality")
        return {'success': False, 'message': 'Must be llama type model.'}
    
    # Clean up existing state if needed
    #if 'state' in app.config and hasattr(app.config['state'], 'cleanup'):
        #app.config['state'].cleanup()

    # Is this a copy?   
    #current_bot = app.config.get['bot_instance']
    #current_bot.change_template(personality)
    #app.config['bot_instance'] = current_bot

    state = app.config.get('state')
    current_bot = state.get('bot_instance')
    print("State in change personalities: ", state , '\n', "current_bot in change personalities: ", current_bot, '\n')
    
    current_bot.change_personality(personality)
    
    #current_bot = state.get('bot_instance')
    print('Current bot now after cahnging personality:', current_bot)
    print('Current personality now after: ', current_bot.personality)
    app.config['bot_instance'] = current_bot
    app.config['state']['personality'] = personality

    
    return {
        'success': True,
        'backend': backend,
        'state': app.config.get('state')
    }

### -------------- Setup -------------- ###

def get_device() -> torch.device:
    """
    Returns the appropriate torch device (GPU if available, otherwise CPU).
    """
    # Check if GPU is available, otherwise sets it to CPU
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

# TODO Maybe split the user and bots convo?
def create_ollama_bot_dict(model_name, bot, backend, max_memory:int=3):
    device = get_device()
    return {
            "model": model_name,  # Just the model name string
            "tokenizer": None,    # Ollama doesn't expose tokenizer
            "bot_instance": bot,   # Keep reference to actual bot
            "personality" : bot.personality,
            "backend": backend,
            "device": device,   # Ollama manages devices internally
            "tts_engine": bot.tts_engine if hasattr(bot, 'tts_engine') else None,
            "chat_history_ids": None,
            "max_memory": max_memory,
        }