import os
from flask import Flask, request, jsonify
from flask_cors import CORS 
from flask import render_template
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from prebuilt.app.chat_bot import get_device, load_model_and_tokenizer, chat_with_bot, trim_chat_history


# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

# Load the model and tokenizer once at the start
#model_name = "microsoft/DialoGPT-medium"  # replace this with your model
model_name = "microsoft/DialoGPT-large"

'''
model_name = "mistralai/Mistral-7B-Instruct-v0.1"

Run this if mac/linux:
export HUGGINGFACE_TOKEN="<huggingface_token_>"
Run this if windows:
$env:HUGGINGFACE_TOKEN="<huggingface_token_>"
'''
token = os.getenv("HUGGINGFACE_TOKEN")  # This fetches the token from your environment

model = AutoModelForCausalLM.from_pretrained(model_name, token=token)
tokenizer = AutoTokenizer.from_pretrained(model_name, token=token)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    chat_history_ids = data.get('chat_history_ids', None)

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    if chat_history_ids:
        chat_history_ids = torch.tensor(chat_history_ids).to(device)

    # Use the shared `chat_with_bot` function
    bot_reply, chat_history_ids = chat_with_bot(user_input, tokenizer, model, chat_history_ids, device)

    return jsonify({
        'response': bot_reply,
        'chat_history_ids': chat_history_ids.tolist()
    })

@app.route('/chat', methods=['POST'])
def chat_here():
    data = request.json
    user_input = data.get('message', '')
    chat_history_ids = data.get('chat_history_ids', None)

    if not user_input:
        return jsonify({'error': 'No message provided'}), 400

    # Encode the new user input, add eos_token, and ensure it uses the right device (GPU/CPU)
    new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt').to(device)

    # If chat_history_ids is provided, convert it to a tensor, otherwise use the new user input
    if chat_history_ids:
        chat_history_ids = torch.tensor(chat_history_ids).to(device)  # Convert to tensor
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)  # Concatenate
    else:
        bot_input_ids = new_user_input_ids  # If no history, use just the new input

    MAX_TOKENS = 10  # or lower
    if chat_history_ids is not None and chat_history_ids.shape[-1] > MAX_TOKENS:
        chat_history_ids = chat_history_ids[:, -MAX_TOKENS:]


    # Generate a response from the model with adjustments
    chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=1000,  # Allow the response to be longer
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,  # Prevent repetitive responses
        top_k=50,  # Top-k sampling for more diverse responses
        top_p=0.95,  # Nucleus sampling for diversity
        temperature=0.7,  # Control randomness
        do_sample=True,  # ENABLE SAMPLING
        num_beams=5,  # Beam search for more coherent responses
        early_stopping=True,  # Stop early if the model reaches a reasonable output
    )

    # Get the bot's reply and decode it
    bot_reply = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Return the bot's reply and the updated chat history
    return jsonify({'response': bot_reply, 'chat_history_ids': chat_history_ids.tolist()})

# Route for testing the app (optional)
@app.route("/")
def home():
    return render_template("index.html")
    #return "Welcome to the chatbot API. Send a POST request to /chat with your message."

if __name__ == "__main__":
    chat_history_ids = None  # Initialize chat history at the start
    app.run(debug=True)  # Run the Flask app in debug mode
