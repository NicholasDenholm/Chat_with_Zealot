import re
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import GPT2LMHeadModel, GPT2Tokenizer


# Define your model architecture
class CustomGPT2(nn.Module):
    def __init__(self):
        super(CustomGPT2, self).__init__()
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")  # Or use your own model architecture here
    
    def forward(self, input_ids):
        return self.model(input_ids)
    
# Define your CustomLSTMModel class to accept the necessary arguments
class CustomLSTMModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim, output_dim):
        super(CustomLSTMModel, self).__init__()
        
        # Define the layers with the appropriate sizes based on the arguments
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, hidden_state=None):
        x = self.embedding(x)  # Apply embedding
        # LSTM layer
        lstm_out, hidden_state = self.lstm(x, hidden_state)
        # Fully connected layer to produce output logits
        output = self.fc(lstm_out)
        return output, hidden_state

def load_vocab(vocab_path):
    """
    Load a vocabulary from a text file and return a dictionary where tokens are mapped to indices.
    
    Parameters:
    - vocab_path: The path to the text file containing the vocabulary.
    
    Returns:
    - vocab_dict: A dictionary where keys are tokens and values are indices.
    """
    # Open and read the file
    with open(vocab_path, 'r') as file:
        vocab = file.readlines()  # Read all lines into a list of strings
    
    # Clean up the vocabulary (remove any extra whitespace and newline characters)
    vocab = [line.strip() for line in vocab]
    
    # Convert the list to a dictionary with token -> index mapping
    vocab_dict = {token: idx for idx, token in enumerate(vocab)}

    print(f"Vocabulary loaded with {len(vocab_dict)} tokens.")
    return vocab_dict

def save_vocab_to_json(vocab_dict, vocab_path):
    """
    Save a vocabulary dictionary to a JSON file.
    
    Parameters:
    - vocab_dict: A dictionary where keys are tokens and values are indices.
    - vocab_path: The path where the vocabulary JSON file will be saved.
    """
    # Save the vocab dictionary to a JSON file
    with open(vocab_path, 'w') as vocab_file:
        json.dump(vocab_dict, vocab_file)
    
    print(f"Vocabulary saved to {vocab_path}")

def generate_reply_k_sample(model, input_text, vocab, max_length=50, temperature=2.0, top_k=5, unk_token = "<unk>"):
    # Tokenize input text using the vocabulary (converting text to indices)
    input_ids = [vocab.get(token, 0) for token in input_text.lower().split()]
    
    # Start with the input sequence and initialize hidden state to None
    hidden_state = None
    generated_ids = input_ids  # Start with input tokens

    # Generate tokens step by step
    for _ in range(max_length):
        # Convert input to tensor, add batch dimension
        input_tensor = torch.tensor(generated_ids).unsqueeze(0)  # Shape: [batch_size, sequence_length]
        
        # Forward pass through the model
        output, hidden_state = model(input_tensor, hidden_state)  # Now it correctly returns hidden_state
        
        # Get the logits for the last token in the sequence
        logits = output[0, -1, :]
        
        # Apply temperature scaling
        logits = logits / temperature
        
        # Apply top-k sampling (keep the top-k logits)
        if top_k > 0:
            top_k_values, top_k_indices = torch.topk(logits, top_k)
            logits = torch.full_like(logits, -float('Inf'))  # Set other values to -inf
            logits[top_k_indices] = top_k_values
        
        # Apply softmax to get probabilities
        probabilities = F.softmax(logits, dim=-1)
        
        # Sample from the distribution
        next_token_id = torch.multinomial(probabilities, 1).item()  # Sample one token

        # Check if the token ID is in the vocabulary, and if not, use <unk>
        if next_token_id not in vocab.values():
            next_token_id = vocab.get(unk_token, 0)  # Fallback to <unk> token
        
        # Add the predicted token to the sequence
        generated_ids.append(next_token_id)
        
        # Stop if the end-of-sequence token is predicted (e.g., assume 0 represents <eos>)
        if next_token_id == vocab.get('<eos>', 0):  # Check for the end-of-sequence token
            break
    
    # Convert token IDs back to text (this will depend on how you store the vocab)
    generated_text = ' '.join([list(vocab.keys())[list(vocab.values()).index(id)] for id in generated_ids])
    return generated_text

def generate_reply(model, input_text, vocab, max_length=50):
    # Tokenize input text using the vocabulary
    input_ids = [vocab.get(token, 0) for token in input_text.lower().split()]  # Assuming space-separated words
    
    # Start with the input sequence and set hidden state to None
    hidden_state = None
    generated_ids = input_ids  # Start with input tokens

    # Generate tokens step by step
    for _ in range(max_length):
        # Convert input to tensor, forward pass
        input_tensor = torch.tensor(generated_ids).unsqueeze(0)  # Add batch dimension
        output, hidden_state = model(input_tensor, hidden_state)  # Get output logits and hidden state

        # Get the predicted next token (highest probability)
        next_token_id = output[0, -1, :].argmax(dim=-1).item()  # Get most likely token

        # Add the predicted token to the sequence
        generated_ids.append(next_token_id)

        # Stop if the end-of-sequence token is predicted (e.g., assume 0 represents <eos>)
        if next_token_id == vocab.get('<eos>', 0):  # Assuming <eos> token is mapped to 0
            break
    
    # Convert token IDs back to text
    generated_text = ' '.join([list(vocab.keys())[list(vocab.values()).index(id)] for id in generated_ids])
    return generated_text

def filter_generated_output(generated_text, unwanted_tokens):
    # Split the generated text into tokens
    generated_tokens = generated_text.split()
    #print(generated_tokens)

    # Remove unwanted tokens
    filtered_tokens = [token for token in generated_tokens if token.lower() not in unwanted_tokens]
    
    # Join the tokens back into a string
    filtered_text = " ".join(filtered_tokens)
    
    return filtered_text

def remove_tokens(generated_text, unwanted_tokens):
    """
    Remove specific tokens/keywords from the generated text.
    
    Parameters:
    - generated_text: The text generated by the model.
    - unwanted_tokens: A list of keywords/phrases to remove from the generated text.
    
    Returns:
    - cleaned_text: The text with unwanted tokens removed.
    """
    
    # Loop through each unwanted token and remove it from the generated text
    for token in unwanted_tokens:
        # Define a regex pattern to match the unwanted token (case insensitive)
        pattern = re.escape(token)  # Escape any special characters in the token
        generated_text = re.sub(pattern, "", generated_text, flags=re.IGNORECASE)
    
    # Optionally clean up extra spaces and strip leading/trailing spaces
    cleaned_text = re.sub(r'\s+', ' ', generated_text).strip()
    
    return cleaned_text

def talk_to_model():
    # Now you can initialize the model with the correct arguments
    model = CustomLSTMModel(vocab_size=560820, embedding_dim=128, hidden_dim=128, output_dim=560820)

    # Load the checkpoint weights into the adjusted model
    checkpoint_path = r'C:\\Users\\nickd\\Desktop\\Code\\warhammerbot\\text_model_2025-03-04_18-48-32.pth'
    checkpoint = torch.load(checkpoint_path)

    # Load the weights
    model.load_state_dict(checkpoint, strict=True)  # strict=True will ensure exact matching of keys and shapes

    # Set the model to evaluation mode
    model.eval()

    vocab_path = r"vocab.json"

    # Call the function to load the vocabulary
    #vocab_dict = load_vocab(vocab_path)

    # Save the vocabulary to the file
    #save_vocab_to_json(vocab_dict, vocab_path)

    with open(vocab_path, 'r') as vocab_file:
        vocab_dict = json.load(vocab_file)

    #print(f"Loaded vocab with {len(vocab_dict)} entries.")
    
    # Set the input text
    input_text = "Hi there."

    # Generate a reply
    reply = generate_reply_k_sample(model, input_text, vocab_dict)
    unwanted_tokens = ['willow', 'road', 'nottingham', 'ng7', '2ws', 'uk', 'uk.', "ack", "www.acklibrary.com", "publishing", "logo", "bl", "fictional", "road, nottingham, 2ws,", "www.games-workshop.com" , "98765432", "tm", "workshop", "2000-2005", "warhammer", "40,000", "www.blacklibrary.com", "games", "and.or", "ltd"]
    #filtered_text = filter_generated_output(reply, unwanted_tokens)
    filtered_text = remove_tokens(reply, unwanted_tokens)
    print("Model Response:", filtered_text)


# _________________________ Others _________________________


def talk_to_GPT2():

    # Initialize the model (you can use your custom architecture here)
    model = CustomGPT2()

    # Load the model weights from the .pth file
    model_path = 'C:\\Users\\nickd\\Desktop\\Code\\warhammerbot\\text_model_2025-03-04_18-48-32.pth'

    # Load the weights into the model
    model.load_state_dict(torch.load(model_path))

    # Set the model to evaluation mode
    model.eval()

    # Load the tokenizer (if using a pre-trained tokenizer like GPT2 tokenizer)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # If you'd like to generate a response from the model, you can do something like this:
    input_text = "Hello, how are you?"
    input_ids = tokenizer.encode(input_text, return_tensors="pt")

    # Generate the response
    with torch.no_grad():
        output = model(input_ids)

    # Decode the output tokens to text
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    print("Model Response:", response)

def test_torch():
        
    data = [1,2,3,4,5,6]
    tensor = torch.tensor(data)
    print((tensor))
    print((tensor.shape))

    x = torch.rand(5, 3)
    print(x)

if __name__ == "__main__":

    try:
        talk_to_model()
        #print("here")    
    except Exception as e:
        print(f"Error occurred: {e}")



