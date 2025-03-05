import torch.nn.functional as F
import all_imports as imp

# Helper function for temperature sampling
def sample_with_temperature(prob_dist, temperature):
    prob_dist = imp.torch.div(prob_dist, temperature)  # Apply temperature scaling
    prob_dist = F.softmax(prob_dist, dim=-1)  # Re-normalize to a valid probability distribution
    return imp.torch.multinomial(prob_dist, 1).item()  # Sample from the distribution

# Helper function for top-k sampling
def sample_top_k(prob_dist, k):
    # Get top-k probabilities and their indices
    top_k_probs, top_k_indices = imp.torch.topk(prob_dist, k)
    top_k_probs = F.softmax(top_k_probs, dim=-1)  # Re-normalize the probabilities
    return imp.torch.multinomial(top_k_probs, 1).item(), top_k_indices

class GenerateText:
    
    def find_n_load_model():
        model_path = imp.g.fileopenbox(msg="Choose your model")

        if model_path:
            model = imp.TextModel(self.vocab_size, self.hidden_size, self.sequence_length)
            # Load the model's state dict from the saved file
            model.load_state_dict(imp.torch.load(self.model_path))
            model = model.to(self.device)  # Move the model to the appropriate device (CPU/GPU)
            return model
        else:
            print("No file selected. Exiting.")
            imp.sys.exit(0)

    @staticmethod
    def generate_text(model, seed_text, sequence_length, num_of_generated_chars, char_to_idx, idx_to_char):
        """
        Generate text from the loaded model.
        """
        generated_text = imp.GenerateText.generate_test(
            model, seed_text, sequence_length, num_of_generated_chars, char_to_idx, idx_to_char
        )
        return generated_text

    @staticmethod
    def generate_test(model, seed, sequence_length, num_generated_chars, char_to_idx, idx_to_char):
        model.eval()
        input_seq = []
        
        # Convert the seed text to indices, and handle missing characters
        for char in seed:
            if char in char_to_idx:
                input_seq.append(char_to_idx[char])
            else:
                print(f"Warning: Character '{char}' not found in vocabulary. Replacing with space.")
                input_seq.append(char_to_idx[' '])  # Replace with space or any other token
        
        input_tensor = imp.torch.tensor(input_seq).unsqueeze(0)  # Add batch dimension

        hidden = None  # Initialize hidden state (if needed by your model)
        generated_text = seed  # Start with the seed text
        temperature = 1.0
        k = 5
        
        # Generate num_generated_chars characters
        for _ in range(num_generated_chars):
            output, hidden = model(input_tensor, hidden)  # Unpack both output and hidden state
            
            predictions = output[:, -1, :]  # Get the predictions for the next character
            prob_dist = F.softmax(predictions / temperature, dim=-1)  # Apply softmax with temperature scaling
            
            # Use temperature-based sampling
            next_char_idx = sample_with_temperature(prob_dist, temperature)  # Call sample_with_temperature here

            # Top-k sampling
            next_char_idx, _ = sample_top_k(prob_dist, k)  # Use top-k sampling to get the next character index
            
            next_char = idx_to_char[next_char_idx]  # Convert the index back to a character
            
            generated_text += next_char  # Append the generated character
            input_tensor = imp.torch.tensor([next_char_idx]).unsqueeze(0)  # Update input for next character
    
        return generated_text