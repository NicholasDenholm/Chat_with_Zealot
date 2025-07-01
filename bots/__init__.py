from bots.zealot_bot import Zealot_Bot
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

