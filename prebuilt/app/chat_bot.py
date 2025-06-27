import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import pyttsx3

def init_chat_state(model_name:str='microsoft/DialoGPT-medium'):
    device = get_device()
    model, tokenizer = load_model_and_tokenizer(model_name, device)
    tts_engine = init_tts_engine(0, rate=200)

    return {
        "model": model,
        "tokenizer": tokenizer,
        "device": device,
        "tts_engine": tts_engine,
        "chat_history_ids": None,
        "max_memory": 3
    }

### -------------- Setup -------------- ###

def get_device() -> torch.device:
    """
    Returns the appropriate torch device (GPU if available, otherwise CPU).
    """
    # Check if GPU is available, otherwise sets it to CPU
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_model_and_tokenizer(model_name:str, device:torch.device):
    """
    Loads the pre-trained model and tokenizer, and moves the model to the specified device.

    Args:
        model_name (str): Name of the pre-trained Hugging Face model.
        device (torch.device): The device to load the model onto.

    Returns:
        tuple: (model, tokenizer)
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
    return model, tokenizer

def load_chat_model(device, model_name="microsoft/DialoGPT-large"):
    token = os.getenv("HUGGINGFACE_TOKEN")
    model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)
    model.to(device)
    return model, tokenizer


### -------------- Chating -------------- ###

def chat_with_bot(user_input: str, tokenizer, model, chat_history_ids=None, device=None):
    """
    Generates a response from the chatbot given a user input.

    Args:
        user_input (str): The input string from the user.
        tokenizer: Hugging Face tokenizer.
        model: Pre-trained transformer model.
        chat_history_ids (torch.Tensor, optional): Tensor of previous chat history. Defaults to None.
        device (torch.device, optional): Device to run the model on. Defaults to None.

    Returns:
        tuple: (bot_reply: str, updated chat_history_ids: torch.Tensor)
    """
    encoded_input = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt").to(device)

    MAX_INPUT_LENGTH = 1024  # or model.config.n_positions

    #bot_input_ids = encoded_input if chat_history_ids is None else torch.cat([chat_history_ids.to(device), encoded_input], dim=-1)
    '''
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=2000,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        temperature=0.8,
        top_p=0.9,
        num_beams=5,
        length_penalty=1.2,
        do_sample=True
    )'''


    if chat_history_ids is None:
        bot_input_ids = encoded_input
    else:
        combined = torch.cat([chat_history_ids.to(device), encoded_input], dim=-1)
        bot_input_ids = combined[:, -MAX_INPUT_LENGTH:]

    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=bot_input_ids.shape[-1] + 150,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        temperature=0.8,
        top_p=0.9,
        num_beams=5,
        length_penalty=1.2,
        do_sample=True
    )

    
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

def trim_chat_history(chat_history_ids, tokenizer, max_turns:int):
    """
    Trims the chat history to only keep the last `max_turns` user-bot exchanges.
    """
    if chat_history_ids is None:
        return None

    decoded = tokenizer.decode(chat_history_ids[0], skip_special_tokens=False)
    # Split by eos_token, and keep last `2 * max_turns` segments (user + bot per turn)
    segments = decoded.split(tokenizer.eos_token)
    trimmed = tokenizer.encode(tokenizer.eos_token.join(segments[-2 * max_turns:]) + tokenizer.eos_token, return_tensors='pt')
    return trimmed

def chat_with_speech(user_input, state):
    bot_reply, state['chat_history_ids'] = chat_with_bot(
        user_input,
        state['tokenizer'],
        state['model'],
        state['chat_history_ids'],
        state['device']
    )
    
    #speak_text(state['tts_engine'], bot_reply) 
    state['chat_history_ids'] = trim_chat_history(
        state['chat_history_ids'],
        state['tokenizer'],
        state['max_memory']
    )
    
    return bot_reply


### -------------- Text to Speech -------------- ###

def init_tts_engine(voice:int=1, rate:int=250):
    """
    Initializes and returns a pyttsx3 TTS engine.
    Args:
        voice (int): 0 for male, 1 for female (may vary by system).
        rate (int): Speech rate (words per minute).
    Returns:
        pyttsx3.Engine: Configured TTS engine.
    """
    if voice not in (0, 1):
        raise ValueError("Voice must be 0 (male) or 1 (female)")
    
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)

    # Change voice
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice].id)
    #print(f"[TTS] Using voice: {voices[voice].name}")

    return engine

def get_available_voices():
    """
    Returns a list of available TTS voices on this machine using pyttsx3.

    Returns:
        List[dict]: List of voice information with keys: index, id, name, language, gender (if available).
    """
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    voice_list = []

    for idx, voice in enumerate(voices):
        voice_info = {
            "index": idx,
            "id": voice.id,
            "name": voice.name,
            "languages": voice.languages if hasattr(voice, "languages") else "unknown",
            "gender": voice.gender if hasattr(voice, "gender") else "unknown"
        }
        voice_list.append(voice_info)

    engine.stop()
    return voice_list

def test_all_voices():
    """
    Tests all available TTS voices by speaking a short phrase for each one.
    """
    voices = get_available_voices()
    engine = pyttsx3.init()

    print("\n🔊 Testing all available voices...\n")

    for v in voices:
        print(f"Index: {v['index']}")
        print(f"  Name    : {v['name']}")
        print(f"  ID      : {v['id']}")
        print(f"  Language: {v['languages']}")
        print(f"  Gender  : {v['gender']}")
        print("  Speaking...\n")

        engine.setProperty('voice', v['id'])
        engine.say("Hello, I am a voice option on this machine.")
        engine.runAndWait()

    engine.stop()
    print("✅ Voice testing completed.")

def speak_text(engine, text: str):
    """
    Uses the pyttsx3 engine to speak the given text.
    
    Args:
        engine (pyttsx3.Engine): Initialized TTS engine.
        text (str): Text to speak.
    """
    engine.say(text)
    engine.runAndWait()


### -------------- MAIN -------------- ###

def main():
    '''
    This runs the model in the terminal, and generates textpyttsx3 to be installed.

    DialoGPT-(smallmedium/large): A model fine-tuned for conversational purposes.
    GPT-2: More general-purpose text generation.
    BART: Another good option for conversational tasks.
    T5: A versatile transformer model that can also be used for dialogues.
    '''
    
    model_name = "microsoft/DialoGPT-large"     # Choose the pre-trained model from above list.
    max_memory = 3                              # Only keep the last 'n' exchanges, lower number reduces logic loops.
    
    device = get_device()
    model, tokenizer = load_model_and_tokenizer(model_name, device)

    # uncomment and run if you want to see the available voices you have on your machine
    #test_all_voices()
    # Text-to-Speech setup, rate is words per minute

    tts_engine = init_tts_engine(0, rate=150)

    chat_history_ids = None     # Initialize chat history

    print("\n---------------------\nChat initialized. Type 'q' to quit.")
    #print()
    
    # Start chatting with the bot
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye!")
            speak_text(tts_engine, "Goodbye!")
            break

        bot_reply, chat_history_ids = chat_with_bot(user_input, tokenizer, model, chat_history_ids, device)
        print(f"Bot: {bot_reply}\n")

        # Speak the bot's reply
        speak_text(tts_engine, bot_reply)

        chat_history_ids = trim_chat_history(chat_history_ids, tokenizer, max_memory)


if __name__ == "__main__":
    main()