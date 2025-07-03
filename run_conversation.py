import os
import random
from bots.dumb_bot import Dumb_Bot
from bots.smart_bot import Smart_Bot
from bots.zealot_bot import Zealot_Bot
from bots.multimodal_bot import Multimodal_Bot
from Ollama.personality import setup_prompts, setup_named_personality, get_all_personality_names, validate_personality_name
from conversation_engine import get_log_path, converse, converse_streaming

# -------------- Bot Builders -------------- #

def build_bots():
    """Initialize and return the two bot instances."""
    dumb = Dumb_Bot("microsoft/DialoGPT-large")

    choice_of_personalities = get_all_personality_names()
    print("List of personalities: ", choice_of_personalities)

    #personality1 = setup_prompts(test=True)
    #personality2 = setup_named_personality('nice_person')
    personality3 = setup_named_personality('expert_coder')
    smart = Smart_Bot(model_name="llama3.2", personality=personality3)

    print("Returning dumb and smart")
    return dumb, smart

def build_dumb_bot(model_name:str):
    """
    Builds a simple prebuilt chatbot using Hugging Face models.
    Available models:
        - "microsoft/DialoGPT-small"
        - "microsoft/DialoGPT-medium"
        - "microsoft/DialoGPT-large"
    """
    supported_models = ["microsoft/DialoGPT-small", "microsoft/DialoGPT-medium", "microsoft/DialoGPT-large"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "microsoft/DialoGPT-medium"
    return Dumb_Bot(model_name)

def build_smart_bot(model_name:str, personality:str):
    """
    Builds a smart bot using Ollama or other supported LLMs.
    Available models:
        - "llama3.2" (default)
        - "mistral", "gemma", "phi3", etc. (extend as needed)
    Personality options (name or tuple supported):
        - "fanatic", "nice_person", "expert_coder", "mean_man", etc.
    """
    supported_models = ["llama3.2", "codellama:7b", "llama3.2:latest"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "llama3.2"
    
    personality = validate_personality_name(personality, fallback="nice_person")
    return Smart_Bot(model_name="llama3.2", personality=personality)

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

#TODO Fix the setup format for the multimodal bot
def build_multimodal_bot(model_name: str = "llava-hf/llava-1.5-7b-hf", personality: str = "fanatic"):
    """
    Builds a multimodal bot with the specified model and personality.

    Available models (examples):
        - "llava-hf/llava-1.5-7b-hf" (default)
        - "llava-hf/llava-1.6-7b-hf"
        - "liuhaotian/llava-v1.5-13b"
        - Add more supported models as needed

    Personality options (validated via `validate_personality_name`):
        - "fanatic", "nice_person", "expert_coder", "mean_man", etc.
    """
    supported_models = ["llava:latest", "llava"]
    if model_name not in supported_models:
        print(f"{model_name} not currently supported falling back to default")
        model_name = "llava"

    personality = validate_personality_name(personality, fallback="fanatic")
    return Multimodal_Bot(model_name=model_name, personality=personality)

def get_bot_combos():
    return {
        "dumb_vs_smart": (
            lambda: build_dumb_bot("microsoft/DialoGPT-medium"),
            lambda: build_smart_bot("llama3.2", "nice_person")
        ),
        "dumb_vs_dumb": (
            lambda: build_dumb_bot("microsoft/DialoGPT-medium"),
            lambda: build_dumb_bot("microsoft/DialoGPT-large")
        ),
        "smart_vs_zealot": (
            lambda: build_smart_bot("llama3.2", "nice_person"),
            lambda: build_zealot_bot("llama3.2", personality="fanatic")
        ),
        "fanatic_vs_preacher": (
            lambda: build_zealot_bot("llama3.2", personality="preacher"),
            lambda: build_zealot_bot("llama3.2", personality="fanatic")
        ),
        "expert_vs_mean": (
            lambda: build_smart_bot("llama3.2", "expert_coder"),
            lambda: build_smart_bot("llama3.2", "mean_person")
        ),
        "smart_vs_smart": (
            lambda: build_smart_bot("llama3.2", "nice_person"),
            lambda: build_smart_bot("llama3.2", "expert_coder")
        ),
        "zealot_vs_dumb": (
            lambda: build_zealot_bot("llama3.2", personality="fanatic"),
            lambda: build_dumb_bot("microsoft/DialoGPT-medium")
        ),
        "zealot_vs_smart": (
            lambda: build_zealot_bot("llama3.2", personality="sermon-lite"),
            lambda: build_smart_bot("llama3.2", "expert_coder")
        ),
        "mean_vs_nice": (
            lambda: build_smart_bot("llama3.2", "mean_person"),
            lambda: build_smart_bot("llama3.2", "nice_person")
        ),
        "sermon_vs_expert": (
            lambda: build_zealot_bot("llama3.2", personality="sermon-lite"),
            lambda: build_smart_bot("llama3.2", "expert_coder")
        )
        # Add more combos here
    }


# -------------- Conversation -------------- #

def run_conversation(bot1, bot2, start_message, rounds, log_to_file=True, extension="md"):
    """Run a bot-to-bot conversation with optional logging."""
    log_path = None

    if log_to_file:
        try:
            # TODO add all of this to the get_log_path method!
            
            print("Current working directory:", os.getcwd())
            log_path, file_type = get_log_path(extension=extension)
            
            #base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this script
            #log_dir = os.path.join(base_dir, "bots", "log")       # project-relative log directory
            #os.makedirs(log_dir, exist_ok=True)                    # make sure it exists

            #log_path = os.path.join(log_dir, f"conversation.{extension}")
            #file_type = extension
            print(f"Logging to: {log_path}")

        except ValueError as e:
            print(f"Error: {e}")
            return

        if file_type == "md":
            converse(bot1, bot2, rounds=rounds, start_message=start_message, log_to_file=True, log_path=log_path, extension=extension)
        elif file_type == "txt":
            converse(bot1, bot2, rounds=rounds, start_message=start_message, log_to_file=True, log_path=log_path, extension=extension)
        elif file_type == "db":
            print("Database logging selected — not implemented yet.")
            # TODO: Add DB conversation function here
        else:
            print("Invalid extension type. Use 'txt', 'md', or 'db'.")
            return
    else:
        converse(bot1, bot2, rounds=rounds, start_message=start_message, log_to_file=False, log_path='', extension='')

def stream_conversation(bot1, bot2, start_message, rounds, stream=True, log_to_file=False, extension="md"):
    """Run a bot-to-bot conversation with optional live streaming and logging."""
    log_path = None

    if log_to_file:
        try:
            print("Current working directory:", os.getcwd())
            log_path, file_type = get_log_path(extension=extension)
            print(f"Logging {file_type} file to: {log_path}")
        except ValueError as e:
            print(f"Error: {e}")
            return
    else:
        file_type = extension

    # Run conversation (this already logs + prints responses)
    messages = converse(
        bot1,
        bot2,
        rounds=rounds,
        start_message=start_message,
        log_to_file=log_to_file,
        log_path=log_path,
        extension=extension
    )

    # If streaming is requested, print a clean, readable stream summary
    if stream:
        print_conversation_stream(messages)

def print_conversation_stream(messages, header=True):
    """Print a clean, readable stream of conversation messages."""
    if header:
        print("\n--- Conversation Stream Recap ---\n")
    for message in messages:
        sender = message["sender"]
        content = message["message"]
        print(f"{sender}: {content}\n")

def stream_conversation_live(bot1, bot2, start_message, rounds, log_to_file=False, extension="md"):
    """Stream conversation live to console while optionally logging."""
    log_path = None

    if log_to_file:
        try:
            print("Current working directory:", os.getcwd())
            log_path, file_type = get_log_path(extension=extension)
            print(f"Logging to: {log_path}")
        except ValueError as e:
            print(f"Error: {e}")
            return

    print("\n--- Live Conversation Stream ---\n")
    for message in converse_streaming(
        bot1, bot2, rounds=rounds,
        start_message=start_message,
        log_to_file=log_to_file,
        log_path=log_path,
        extension=extension
    ):
        sender = message["sender"]
        content = message["message"]
        print(f"{sender}: {content}\n")

# -------------- Selctiing combos -------------- #

def test_all_combos():
    combos = get_bot_combos()
    for combo_name, (build_bot1, build_bot2) in combos.items():
        print(f"\n=== Running combo: {combo_name} ===")
        bot1 = build_bot1()
        bot2 = build_bot2()
        start_message = "Begin the conversation."
        run_conversation(
            bot1=bot1,
            bot2=bot2,
            start_message=start_message,
            rounds=5,
            log_to_file=False,
            extension="md"
        )

def choose_combo(start_message:str, rounds:int, log_to_file:bool, extension:str):
    combos = get_bot_combos()
    names = list(combos.keys())

    print("Choose a bot combo:")
    for i, name in enumerate(names, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("Enter a number: ")) - 1
        if 0 <= choice < len(names):
            combo_name = names[choice]
            build_bot1, build_bot2 = combos[combo_name]
            bot1 = build_bot1()
            bot2 = build_bot2()
            run_conversation(
                bot1=bot1,
                bot2=bot2,
                start_message=start_message,
                rounds=rounds,
                log_to_file=log_to_file,
                extension="md"
            )
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")

def test_random_combo(start_message:str, rounds:int, log_to_file:bool, extension:str):
    combos = get_bot_combos()
    #combo_name, (build_bot1, build_bot2) = random.choice(list(combos.items()))
    rand_combo = random.choice(list(combos.items()))
    combo_name = rand_combo[0]
    print(f"Running random combo: {combo_name}")
    build_bot1, build_bot2 = combos[combo_name]
    bot1 = build_bot1()
    bot2 = build_bot2()
    run_conversation(
        bot1=bot1,
        bot2=bot2,
        start_message=start_message,
        rounds=rounds,
        log_to_file=log_to_file,
        extension=extension
    )

# -------------- Main -------------- #

def main(mode="choose"):
    combos = get_bot_combos()

    start_message = "What heresy do you bring?"
    rounds = 5
    log_to_file = True
    extension = 'md'

    if mode == "choose":
        choose_combo(start_message, rounds, log_to_file, extension)  # Interactive selection
    elif mode == "random":
        test_random_combo(start_message, rounds, log_to_file, extension) # Random selection
    elif mode == "all":
        test_all_combos()
    elif mode in combos:
        # Directly run a specific combo by name
        print(f"Running specific combo: {mode}")
        build_bot1, build_bot2 = combos[mode]
        bot1 = build_bot1()
        bot2 = build_bot2()
        run_conversation(bot1=bot1, bot2=bot2, start_message="Begin the conversation.", rounds=10, log_to_file=True, extension="md")
        # TODO: test these:
        #stream_conversation(dumb=dumb, smart=smart, start_message=start_message, rounds=rounds, log_to_file=log_to_file, extension=log_extension)
        #stream_conversation_live(dumb=dumb, smart=smart, start_message=start_message, rounds=rounds, log_to_file=log_to_file, extension=log_extension)
    else:
        print(f"[Error] Invalid mode or combo name: '{mode}'") # Options: 'md', 'txt', 'db'
        print(f"Valid options: 'choose', 'random', 'all', or one of: {list(combos.keys())}")


if __name__ == "__main__":
    #main()  # old methodology
    main("choose")         # Opens CLI menu
    #main("random")       # Runs a random combo
    #main("all")          # Tests all combos
    #main("smart_vs_zealot")  # Runs that specific combo