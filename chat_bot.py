import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


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
    bot_input_ids = encoded_input if chat_history_ids is None else torch.cat([chat_history_ids, encoded_input], dim=-1)

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

def main():
    '''
    DialoGPT: A model fine-tuned for conversational purposes.
    GPT-2: More general-purpose text generation.
    BART: Another good option for conversational tasks.
    T5: A versatile transformer model that can also be used for dialogues.
    '''
    # Load the pre-trained model and tokenizer
    model_name = "microsoft/DialoGPT-medium"
    device = get_device()
    model, tokenizer = load_model_and_tokenizer(model_name, device)

    
    chat_history_ids = None     # Initialize chat history
    max_memory = 3              # Only keep the last 'n' exchanges in chat_history_ids

    print("\n---------------------")
    print("\nChat initialized. Type 'q' to quit.")
    
    # Start chatting with the bot
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye!")
            break

        bot_reply, chat_history_ids = chat_with_bot(user_input, tokenizer, model, chat_history_ids)
        print(f"Bot: {bot_reply}\n")
        chat_history_ids = trim_chat_history(chat_history_ids, tokenizer, max_memory)


if __name__ == "__main__":
    main()