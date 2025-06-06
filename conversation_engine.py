import datetime
import os

### --------------- Setup --------------- ###

def get_log_path(log_to_file:bool=True, log_path=None, extension:str='txt') -> str:
    if not log_to_file:
        return None
    if log_path is not None:
        return log_path 
    # Ensure the log directory exists
    #log_dir = os.path.join("bots", "log")
    #os.makedirs(log_dir, exist_ok=True)

    base_dir = os.path.dirname(os.path.abspath(__file__))  # directory of this script
    log_dir = os.path.join(base_dir, "bots", "log")       # project-relative log directory
    os.makedirs(log_dir, exist_ok=True)                    # make sure it exists

    #log_path = os.path.join(log_dir, f"conversation.{extension}")

    # Otherwise create timestamped name and set log path
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(log_dir, f"conversation_log_{timestamp}.{extension}"), extension


def make_header(log_path: str, start_message: str, rounds:str, extension:str):
    if not log_path:
        raise ValueError("log_path must be provided to create the log header.")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    if extension == "txt":
        with open(log_path, "w", encoding="utf-8") as f:
            f.write("Bot-to-Bot Conversation Log\n")
            f.write(f"Start Time: {datetime.datetime.now()}\n")
            f.write(f"Number of rounds: {rounds}\n")
            f.write(f"Starting message: {start_message}\n")
            f.write(f"________________________________________")
            f.write(f"\n\n")
    
    if extension == "md":
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"# Bot-to-Bot Conversation Log\n")
            f.write(f"**Start Time**: {datetime.datetime.now()}\n")
            f.write(f"**Starting message:**: `{start_message}`\n")
            f.write(f"________________________________________")
            f.write(f"\n\n")
        

### --------------- Chatting --------------- ###

def converse(bot1, bot2, rounds=6, start_message="Hello", log_to_file=True, log_path=None, extension:str='txt'):
    messages = [{"sender": "user", "message": start_message}]
    current_bot = bot1

    if log_to_file:
        rounds_str = str(rounds)
        if log_path:
            make_header(log_path, start_message, rounds_str, extension)


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
