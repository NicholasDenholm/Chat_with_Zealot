import os
from bots.dumb_bot import Dumb_Bot
from bots.smart_bot import Smart_Bot
from Ollama.personality import setup_prompts
from conversation_engine import converse, get_log_path


def build_bots():
    """Initialize and return the two bot instances."""
    dumb = Dumb_Bot("microsoft/DialoGPT-large")

    personality = setup_prompts(test=True)
    smart = Smart_Bot(model_name="llama3.2", personality=personality)

    return dumb, smart


def run_conversation(dumb, smart, start_message, rounds, log_to_file=True, extension="md"):
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
            converse(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=True, log_path=log_path, extension=extension)
        elif file_type == "txt":
            converse(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=True, log_path=log_path, extension=extension)
        elif file_type == "db":
            print("Database logging selected — not implemented yet.")
            # TODO: Add DB conversation function here
        else:
            print("Invalid extension type. Use 'txt', 'md', or 'db'.")
            return
    else:
        converse(dumb, smart, rounds=rounds, start_message=start_message)


def main():
    dumb, smart = build_bots()
    start_message = "What heresy do you bring?"
    rounds = 6
    log_to_file = False
    log_extension = "md"  # Options: 'md', 'txt', 'db'

    run_conversation(dumb=dumb, smart=smart, start_message=start_message, rounds=rounds, log_to_file=log_to_file, extension=log_extension)


if __name__ == "__main__":
    main()