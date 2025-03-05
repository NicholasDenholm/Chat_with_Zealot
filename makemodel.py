import all_imports as imp

class ModelTrainer:
    
    @staticmethod
    def train_and_generate_text(batch_size, sequence_length, hidden_size, num_epochs, learning_rate, dataloader, vocab_size):
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

        output_path = load_inst.set_output_folder()
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
