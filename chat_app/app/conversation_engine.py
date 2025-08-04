import datetime
import os

### --------------- Setup --------------- ###

def get_log_path(log_to_file:bool=True, log_path=None, extension:str='txt') -> str:
    if not log_to_file:
        return None
    if log_path is not None:
        return log_path 

    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    log_dir = os.path.join(base_dir, "bots", "log")       # project-relative log directory
    os.makedirs(log_dir, exist_ok=True)                    # make sure it exists

    #log_path = os.path.join(log_dir, f"conversation.{extension}")

    # Otherwise create timestamped name and set log path
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(log_dir, f"conversation_log_{timestamp}.{extension}"), extension

def make_header(log_path: str, start_message: str, rounds:str, extension:str, bots:list):
    if not log_path:
        raise ValueError("log_path must be provided to create the log header.")

    # Unpack the bots
    bot1, bot2 = bots

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    if extension == "txt":
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("Bot-to-Bot Conversation Log\n")
            f.write(f"Start Time: {datetime.datetime.now()}\n")
            f.write(f"Bot 1: {describe_bot(bot1)}\n")
            f.write(f"Bot 2: {describe_bot(bot2)}\n")
            f.write(f"Number of rounds: {rounds}\n")
            f.write(f"Starting message: {start_message}\n")
            f.write(f"________________________________________")
            f.write(f"\n\n")
    
    if extension == "md":
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Bot-to-Bot Conversation Log\n")
            f.write(f"# Start Time: {datetime.datetime.now()}\n")
            f.write(f"# Bot 1: {describe_bot(bot1)}\n")
            f.write(f"# Bot 2: {describe_bot(bot2)}\n")
            f.write(f"# Number of rounds: {rounds}\n")
            f.write(f"# Starting message: `{start_message}`\n")
            f.write(f"________________________________________")
            f.write(f"\n\n")
        
def describe_bot(bot):
    """Returns the name and persona of a given bot"""
    name = getattr(bot, "model_name", "unknown_model")
    persona = getattr(bot, "personality", None)
    if isinstance(persona, tuple):
        persona = ", ".join(persona)
    return f"{bot.__class__.__name__} (model: {name}, personality: {persona})"

### --------------- Chatting --------------- ###

def converse(bot1, bot2, rounds:int, start_message:str, log_to_file:str, log_path:str, extension:str):
    messages = [{"sender": "user", "message": start_message}]
    current_bot = bot1

    if log_to_file:
        rounds_str = str(rounds)
        if log_path:
            bots = [bot1, bot2]
            make_header(log_path, start_message, rounds_str, extension, bots)


    for i in range(rounds):
        last_message = messages[-1]["message"]
        response = current_bot.reply(last_message)

        sender_name = current_bot.__class__.__name__
        messages.append({"sender": sender_name, "message": response})

        print(f"{sender_name}: {response}\n")

        if log_to_file:
            with open(log_path, "a", encoding="utf-8") as f:
                if extension == "txt":
                    f.write(f"{sender_name}: {response}\n\n")
                if extension == "md":
                    f.write(f"### {sender_name}\n")
                    f.write(f"> {response.strip()}\n\n")


        # Alternate between bots
        current_bot = bot2 if current_bot == bot1 else bot1

    return messages


def converse_no_log(bot1, bot2, rounds:int, start_message:str):
    messages = [{"sender": "user", "message": start_message}]
    current_bot = bot1

    for i in range(rounds):
        last_message = messages[-1]["message"]
        response = current_bot.reply(last_message)

        sender_name = current_bot.__class__.__name__
        messages.append({"sender": sender_name, "message": response})

        print(f"{sender_name}: {response}\n")

        # Alternate between bots
        current_bot = bot2 if current_bot == bot1 else bot1

    return messages

def converse_streaming(bot1, bot2, rounds=6, start_message="Hello", log_to_file=True, log_path=None, extension='txt'):
    """Stream a bot-to-bot conversation in real-time via generator."""
    current_bot = bot1
    message = start_message

    if log_to_file and log_path:
        rounds_str = str(rounds)
        make_header(log_path, start_message, rounds_str, extension)

    yield {"sender": "user", "message": start_message}

    for i in range(rounds):
        response = current_bot.reply(message)
        sender_name = current_bot.__class__.__name__

        yield {"sender": sender_name, "message": response}

        if log_to_file and log_path:
            with open(log_path, "a", encoding="utf-8") as f:
                if extension == "txt":
                    f.write(f"{sender_name}: {response}\n\n")
                elif extension == "md":
                    f.write(f"### {sender_name}\n> {response.strip()}\n\n")

        # Prepare for next round
        message = response
        current_bot = bot2 if current_bot == bot1 else bot1
