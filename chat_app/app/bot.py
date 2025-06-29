import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from prebuilt.app.chat_bot import init_chat_state

def init_model_state(backend: str = 'huggingface', model_name: str = None, device: str = None):
    # TODO setup prebuilt 
    # ##TODO setup whisper speech recog 
    

    if backend == "huggingface":
        state = init_chat_state()
        #print("Type of state:", type(state))
        #print("State value:", state)
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

'''
def load_llamacpp_model(model_path):
    from llama_cpp import Llama
    return Llama(model_path=model_path)
    '''