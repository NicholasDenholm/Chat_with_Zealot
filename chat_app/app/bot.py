import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from prebuilt.app.chat_bot import init_chat_state
import bots

def init_model_state(backend: str = 'huggingface', model_name: str = None, device: str = None):
    
    if backend == "huggingface":
        state = init_chat_state()
        #print("Type of state:", type(state))
        #print("State value:", state)
        return state
    
    elif backend == "llamacpp":
        
        #bot = bots.build_zealot_bot(model_name, 'fanatic')
        bot = bots.build_zealot_bot(model_name, 'short_answers')
        max_memory = 3
        
        state = create_ollama_bot_dict(bot.model_name, bot, backend, max_memory)
        print(state, "\n")

        return state
    else: 
        raise ValueError(f"Unsupported backend: {backend}")
    
    
    
    # TODO set up zealot bot
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

    elif backend == "llamacpp":
        model_path = model_name or "./models/llama.bin"
        model = load_llamacpp_model(model_path)
        return {
            "backend": backend,
            "model": model,
            "tts_engine": tts_engine,
        }
    '''
    



### -------------- Setup -------------- ###

def get_device() -> torch.device:
    """
    Returns the appropriate torch device (GPU if available, otherwise CPU).
    """
    # Check if GPU is available, otherwise sets it to CPU
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def create_ollama_bot_dict(model_name, bot, backend, max_memory:int=3):
    device = get_device()
    return {
            "model": model_name,  # Just the model name string
            "tokenizer": None,    # Ollama doesn't expose tokenizer
            "bot_instance": bot,   # Keep reference to actual bot
            "backend": backend,
            "device": "ollama",   # Ollama manages devices internally
            "tts_engine": bot.tts_engine if hasattr(bot, 'tts_engine') else None,
            "chat_history_ids": None,
            "max_memory": max_memory,
        }