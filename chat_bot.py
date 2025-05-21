import torch

from transformers import AutoModelForCausalLM, AutoTokenizer

# Check if GPU is available and set device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

'''
DialoGPT: A model fine-tuned for conversational purposes.
GPT-2 or GPT-3: You can use these for more general-purpose text generation.
BART: Another good option for conversational tasks.
T5: A versatile transformer model that can also be used for dialogues.
'''
# Load the pre-trained model and tokenizer
model_name = "microsoft/DialoGPT-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Move the model to the selected device (GPU or CPU)
model.to(device)

# Function to chat with the model over the terminal
def chat_with_bot(user_input, chat_history_ids=None):
    # Encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

    # Append the new user input tokens to the chat history (if any)
    bot_input_ids = new_user_input_ids if chat_history_ids is None else torch.cat([chat_history_ids, new_user_input_ids], dim=-1)

    # Generate a response with extended settings
    chat_history_ids = model.generate(
        bot_input_ids,
        max_length=2000,        # Longer responses
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3, # Avoid repetition
        temperature=0.8,        # More creativity/randomness
        top_p=0.9,              # Use nucleus sampling
        num_beams=5,            # Beam search for better quality
        length_penalty=1.2      # Encourage longer responses
    )

    # Get the bot's reply and decode it
    bot_reply = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    return bot_reply, chat_history_ids

# Initialize chat history
chat_history_ids = None

# Start chatting with the bot
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        break

    bot_reply, chat_history_ids = chat_with_bot(user_input, chat_history_ids)
    print(f"Bot: {bot_reply}\n")