import all_imports as imp

class ModelTrainer:
    
    @staticmethod
    def train_and_generate_text(batch_size, sequence_length, hidden_size, num_epochs, learning_rate, dataset, dataloader, vocab_size):
        """
        Train a model and generate text after training. This is a static method.
        """
        
        if imp.torch.cuda.is_available():
            device = imp.torch.device('cuda')
            print(f'CUDA is available. Using device: {imp.torch.cuda.get_device_name(0)}')
        else:
            device = imp.torch.device('cpu')
            print('CUDA is not available. Using CPU.')

        model = imp.TextModel(vocab_size, hidden_size, sequence_length)
        model = model.to(device)  # Move the model to the correct device (GPU or CPU)

        criterion = imp.nn.CrossEntropyLoss()
        optimizer = imp.optim.Adam(model.parameters(), lr=learning_rate)
        scheduler = imp.torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

        output_path = imp.Loading.set_output_folder()
        current_date = imp.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  

        # Train the model and save it after each epoch
        for epoch in range(num_epochs):
            print(f"Epoch {epoch+1}/{num_epochs}")

            # Train for one epoch
            imp.Train.train(model, dataloader, criterion, optimizer, 1, device)  # Only one epoch at a time

            # Save the model after each epoch
            model_save_path = imp.os.path.join(output_path, f'text_model_epoch_{epoch+1}_{current_date}.pth')
            imp.torch.save(model.state_dict(), model_save_path)
            print(f"Model saved at: {model_save_path}")

        # Generate text after training
        seed_text = "Once upon a time"
        num_of_generated_chars = 50  # How many characters to generate
        generated_text = imp.GenerateText.generate_test(model, seed_text, sequence_length, num_of_generated_chars, dataset.char_to_idx, dataset.idx_to_char)
        print(generated_text)

    @staticmethod
    def load_and_resize_model(model, model_path, current_vocab_size, device):
        # Load pre-trained weights
        pre_trained_weights = imp.torch.load(model_path)

        # Get the embedding weights from the pre-trained model
        pretrained_embedding_weights = pre_trained_weights.get('embedding.weight')
        pretrained_fc_weights = pre_trained_weights.get('fc.weight')
        pretrained_fc_bias = pre_trained_weights.get('fc.bias')

        # Resize the embedding weights to match the current vocabulary size (padding or trimming)
        if pretrained_embedding_weights is not None:
            old_vocab_size, embedding_dim = pretrained_embedding_weights.size()
            new_vocab_size = current_vocab_size

            # Resize embedding layer (pad or trim weights)
            if new_vocab_size > old_vocab_size:
                # Pad the embedding layer with zeros if the new vocab size is larger
                padding = imp.torch.zeros(new_vocab_size - old_vocab_size, embedding_dim)
                resized_embedding_weights = imp.torch.cat([pretrained_embedding_weights, padding], dim=0)
            elif new_vocab_size < old_vocab_size:
                # Trim the embedding layer if the new vocab size is smaller
                resized_embedding_weights = pretrained_embedding_weights[:new_vocab_size, :]
            else:
                resized_embedding_weights = pretrained_embedding_weights

            # Replace the original embedding weights in the model
            model.embedding.weight.data = resized_embedding_weights

        # Resize the fully connected layer weights (pad or trim if necessary)
        if pretrained_fc_weights is not None:
            old_fc_size, _ = pretrained_fc_weights.size()
            new_fc_size = current_vocab_size

            # Resize fully connected layer (pad or trim weights)
            if new_fc_size > old_fc_size:
                # Pad the fc layer with zeros if the new vocab size is larger
                padding = imp.torch.zeros(new_fc_size - old_fc_size, pretrained_fc_weights.size(1))
                resized_fc_weights = imp.torch.cat([pretrained_fc_weights, padding], dim=0)
            elif new_fc_size < old_fc_size:
                # Trim the fully connected layer if the new vocab size is smaller
                resized_fc_weights = pretrained_fc_weights[:new_fc_size, :]
            else:
                resized_fc_weights = pretrained_fc_weights

            # Replace the original fully connected layer weights in the model
            model.fc.weight.data = resized_fc_weights
            model.fc.bias.data = pretrained_fc_bias[:new_fc_size]  # Resize bias if necessary

        # Return the model with the resized weights
        model = model.to(device)
        return model

