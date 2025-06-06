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
            log_path, file_type = get_log_path(log_to_file=log_to_file,log_dir="./bots/log",extension=extension)
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

    run_conversation(dumb=dumb,smart=smart,start_message=start_message,rounds=rounds,log_to_file=log_to_file,extension=log_extension)

    '''
    dumb = Dumb_Bot('microsoft/DialoGPT-large')

    personality = setup_prompts(test=True)      # test=True chooses first option
    smart = Smart_Bot(model_name="llama3.2", personality=personality)

    start_message = "What heresy do you bring?"
    rounds = 6

    # Set to true if you want to save the conversation
    log_to_file = True
    
    if log_to_file:
        # Change extension to txt, md, db
        log_path, extension = get_log_path(log_to_file, '.bots\log', extension='md')
        if extension == "md":
            converse(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=log_to_file, log_path=log_path, extension=extension)
        elif extension == "txt":
            converse(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=log_to_file, log_path=log_path, extension=extension)
        elif extension == "db":
            print("db choosen")
        else:
            print("Choose from logging file types, txt, md, db")
    else: 
        log_path = None
        # Start converstation
        converse(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=log_to_file, log_path=log_path)

    converse_md(dumb, smart, rounds=rounds, start_message=start_message, log_to_file=log_to_file, log_path=log_path)
    '''

if __name__ == "__main__":
    main()