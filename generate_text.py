class Generate_Text():
    
    def generate_text(model, seed, sequence_length, num_generated_chars, char_to_idx, idx_to_char):
        model.eval()
        input_seq = [char_to_idx[char] for char in seed]
        input_tensor = torch.tensor(input_seq).unsqueeze(0)  # Add batch dimension
        
        generated_text = seed
        for _ in range(num_generated_chars):
            with torch.no_grad():
                output = model(input_tensor)
                output = output[:, -1, :]  # Get the last time step's output
                predicted_idx = torch.argmax(output, dim=1).item()
                predicted_char = idx_to_char[predicted_idx]
                generated_text += predicted_char
                input_tensor = torch.cat((input_tensor, torch.tensor([[predicted_idx]])), dim=1)[:, 1:]

        return generated_text