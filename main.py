import all_imports as imp

def main():

    batch_size = 12
    sequence_length = 64
    hidden_size = 128
    num_epochs = 1
    learning_rate = 0.001

    print(f"Hello, your batch size is: {batch_size}, seq length: {sequence_length}, and hidden size: {hidden_size}")
        
    load_inst = imp.Loading()
    file_path = load_inst.load_data_box()
    print(f"Data from: {file_path} was loaded")

    text = load_inst.load_n_process_data()
    dataset = imp.TextDataset(text, sequence_length)
    print(f"Dataset size: {len(dataset)}")

    dataloader = imp.torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=6, shuffle=True)
    print(f"Dataloader size: {len(dataloader)}")
    vocab_size = len(dataset)
    if imp.torch.cuda.is_available():
        device = imp.torch.device('cuda')
    else:
        device = imp.torch.device('cpu')

    # Create and show the choicebox options
    choices = ["Generate Text", "Train a New Model", "Retrain an Existing Model"]
    choice = imp.g.choicebox("Choose an action", choices=choices)

    if choice == "Generate Text":
        print("Generating text from a premade model...")

        model = imp.GenerateText.find_n_load_model(vocab_size, hidden_size, sequence_length, device)
        num_of_generated_chars = 300

        while True:
            # Set seed text
            seed_text = input("Enter a seed text for generation (or 'exit' to quit): ").strip()
            seed_text.lower()

            if seed_text == 'exit':
                print("Exiting the program.")
                break  # Exit the loop if the user types 'exit'

            num_of_generated_chars = 50  # Number of characters to generate

            # Generate the text based on the seed text
            generated_text = imp.GenerateText.generate_test(
                model,
                seed_text,
                sequence_length,
                num_of_generated_chars,
                dataset.char_to_idx,
                dataset.idx_to_char
            )

            print(f">>> {generated_text}")

    elif choice == "Train a New Model":
        
        print("Training a new model...")
        imp.ModelTrainer.train_and_generate_text(batch_size, sequence_length, hidden_size, num_epochs, learning_rate, dataset, dataloader, vocab_size)  

    elif choice == "Retrain an Existing Model":
        print("Retraining an existing model...")

        model_path = "text_model_2025-03-04_18-48-32.pth"

        output_path = imp.Loading.set_output_folder()
        current_date = imp.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  

        cur_vocab_size = len(dataset)
        model = imp.GenerateText.find_n_load_model(cur_vocab_size, hidden_size, sequence_length, device)
        #pre_trained_weights = imp.torch.load(model_path)
        # Only load weights for matching layers
        #model.load_state_dict(pre_trained_weights, strict=False)  
        model = model.to(device) 



        try:
            model = imp.ModelTrainer.load_and_resize_model(model, model_path, cur_vocab_size, device)
            print("Model loaded and resized successfully.")

        except Exception as e:
            print(f"Error occurred: {e}")

        optimizer = imp.optim.Adam(model.parameters(), lr=learning_rate)
        criterion = imp.nn.CrossEntropyLoss()
        #scheduler = imp.torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

        # Define the optimizer and loss function for fine-tuning
        #optimizer = imp.torch.optim.Adam(model.parameters(), lr=learning_rate)
        #criterion = imp.torch.nn.CrossEntropyLoss()

        
        # Train the model and save it after each epoch
        for epoch in range(num_epochs):
            print(f"Epoch {epoch+1}/{num_epochs}")

            # Single epoch retraining
            retrain_instance = imp.Train()
            retrain_instance.train(model, dataloader, criterion, optimizer, num_epochs, device)

            # Save the retrained model after each epoch
            model_save_path = imp.os.path.join(output_path, f'Retrained_model_epoch_{epoch+1}_{current_date}.pth')
            imp.torch.save(model.state_dict(), model_save_path)
            print(f"Model saved at: {model_save_path}")

if __name__ == '__main__':
    
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
    
