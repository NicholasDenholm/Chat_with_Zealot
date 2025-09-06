from bots.zealot_bot import Zealot_Bot
from bots.smart_bot import Smart_Bot
from bots.whisper_bot import Whisper_Bot, pick_language
from bots.multimodal_bot import build_multimodal_bot
from Ollama.personality import validate_personality_name

def build_zealot_bot(model_name:str, personality:str):
    """
    Initializes a Zealot-themed chat bot using an Ollama model.

    Model options:
        - "llama3.2" (default)
        - Extend with others if supported (e.g., "mistral", "phi3", etc.)

    Personality options (name or tuple):
        - "fanatic", "preacher", "sermon-lite"
        - Or use a custom personality tuple (length, style, emotionality)
    """
    supported_models = ["llama3.2", "codellama:7b", "llama3.2:latest"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "llama3.2"

    personality = validate_personality_name(personality, fallback="fanatic")
    return Zealot_Bot(model_name="llama3.2", personality=personality)


def build_smart_bot(model_name:str, personality:str):
    """
    Initializes a chat bot using an Ollama model.

    Model options:
        - "llama3.2" (default)
        - Extend with others if supported (e.g., "mistral", "phi3", etc.)

    Personality options (name or tuple):
        - "nice_person", "expert_coder", "short_answers", "mean_person"
        - Or use a custom personality tuple (length, style, emotionality)
    """
    supported_models = ["llama3.2", "codellama:7b", "llama3.2:latest"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "llama3.2"

    personality = validate_personality_name(personality, fallback="short_answers")
    return Smart_Bot(model_name="llama3.2", personality=personality)


def build_coding_bot(model_name:str, personality:str):
    # TODO add more coding functionality to this bot
    """
    Initializes a chat bot using an Ollama model.

    Model options:
        - "codellama:7b" (default)
        - Extend with others if supported (e.g., "mistral", "phi3", etc.)

    Personality options (name or tuple):
        - "expert_coder", .. extend this
        - Or use a custom personality tuple (length, style, emotionality)
    """
    supported_models = ["llama3.2", "codellama:7b", "llama3.2:latest"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "codellama:7b"

    personality = validate_personality_name(personality, fallback="expert_coder")
    return Smart_Bot(model_name="codellama:7b", personality=personality)


# TODO test and add params to these two functions!
def build_whisper_bot():
    
    bot = Whisper_Bot(model_name="medium")
    fs = 16000  # Sample rate
    language_code = pick_language() # ISO code
    bot.set_language(language_code)

    return bot

def build_vision_bot():

    bot = build_multimodal_bot(model_name='llava', user_request=2)
    return bot
