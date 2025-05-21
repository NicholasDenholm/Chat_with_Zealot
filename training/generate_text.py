import torch.nn.functional as F
import all_imports as imp

class GenerateText:

    # Helper function for temperature sampling
    def sample_with_temperature(prob_dist, temperature):
        """
        Sample a character index from the probability distribution using temperature scaling.
        """
        # Sample for each row in the batch
        batch_size = prob_dist.size(0)
        
        # Sample one index for each element in the batch
        next_char_idx = imp.torch.multinomial(prob_dist, 1)  # Shape will be (batch_size, 1)
        next_char_idx = next_char_idx.squeeze()  # Remove the extra dimension (batch_size,)
        
        return next_char_idx # Return the first sampled index (for a single element)

    # Helper function for top-k sampling
    def sample_top_k(prob_dist, k):
        # Get top-k probabilities and their indices
        top_k_probs, top_k_indices = imp.torch.topk(prob_dist, k)
        top_k_probs = F.softmax(top_k_probs, dim=-1)  # Re-normalize the probabilities
        return imp.torch.multinomial(top_k_probs, 1).item(), top_k_indices
    
    def find_n_load_model(vocab_size, hidden_size, sequence_length, device):
        model_path = imp.g.fileopenbox(msg="Choose your model")

        if model_path:
            model = imp.TextModel(vocab_size, hidden_size, sequence_length)
            # Load the model's state dict from the saved file
            model.load_state_dict(imp.torch.load(model_path))
            model = model.to(device)  # Move the model to the appropriate device (CPU/GPU)
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
    def generate_test(model, seed_text, sequence_length, num_of_generated_chars, char_to_idx, idx_to_char, temperature=0.7, k=5):
        
        # Check if CUDA is available
        if imp.torch.cuda.is_available():
            device = imp.torch.device('cuda')
        else:
            device = imp.torch.device('cpu')
        
        model = model.to(device)
        model.eval()  # Set model to evaluation mode
        input_seq = []

        # Convert the seed text to indices, and handle missing characters
        for char in seed_text:
            if char in char_to_idx:
                input_seq.append(char_to_idx[char])
            else:
                print(f"Warning: Character '{char}' not found in vocabulary. Replacing with space.")
                input_seq.append(char_to_idx[' '])  # Replace with space or any other token
        
        # Convert the seed to a tensor and move it to the appropriate device
        input_tensor = imp.torch.tensor(input_seq).unsqueeze(0).to(device)  # Add batch dimension
        
        hidden = None  # Initialize hidden state (if needed by your model)
        generated_text = seed_text  # Start with the seed text

        for _ in range(num_of_generated_chars):
            output, hidden = model(input_tensor, hidden)  # Get the model output and update the hidden state
            output = output.squeeze(0)  # Remove batch dimension

            #print(f"Output shape: {output.shape}")  # Print the shape to debug
            # If output has shape (batch_size, vocab_size), handle directly
            if len(output.shape) == 2:  # This means it's (batch_size, vocab_size)
                predictions = output  # Directly use the output for predictions
            elif len(output.shape) == 3:  # This means it's (batch_size, seq_len, vocab_size)
                predictions = output[:, -1, :]  # Get the predictions for the next character

            prob_dist = F.softmax(predictions / temperature, dim=-1)  # Apply softmax with temperature scaling
            
            # Use temperature-based sampling 
            next_char_idx = GenerateText.sample_with_temperature(prob_dist, temperature)
            # or top-k sampling
            #next_char_idx, _ = GenerateText.sample_top_k(prob_dist, k)  # Use top-k sampling to get the next character index

            # Handle the next_char_idx correctly (if it's a tensor with multiple indices)
            if isinstance(next_char_idx, imp.torch.Tensor):
                next_char_idx = next_char_idx.tolist()  # Convert to a list of indices (for batch or multi-index tensor)
            
            #print(f"Sampled next_char_idx: {next_char_idx}")

            # If next_char_idx is a single index (integer), convert it to a list for consistency
            if isinstance(next_char_idx, int):
                next_char_idx = [next_char_idx]  # Make it a list with a single element

            # Convert indices to corresponding characters
            next_char = ''.join([idx_to_char[idx] for idx in next_char_idx])
            
            # Append the generated character to the result
            generated_text += next_char  # Append the generated character

            # Update input_tensor for the next iteration with the next character index
            input_tensor = imp.torch.tensor([[next_char_idx[-1]]]).to(device)  # Use the last sampled index for the next iteration

        return generated_text