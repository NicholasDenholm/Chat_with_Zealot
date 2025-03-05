import all_imports as imp

def main():

    batch_size = 12
    sequence_length = 64
    hidden_size = 128
    num_epochs = 3
    learning_rate = 0.001

    print(f"Hello, your batch size is: {batch_size}, seq length: {sequence_length}, and hidden size: {hidden_size}")
        
    load_inst = imp.Loading()
    file_path = load_inst.load_data_box()
    print(f"Data from: {file_path} was loaded")

    text = load_inst.load_n_process_data()
    dataset = imp.TextDataset(text, sequence_length)

    dataloader = imp.torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=6, shuffle=True)
    vocab_size = len(dataset)

    # Create and show the choicebox options
    choices = ["Generate Text", "Train a New Model", "Retrain and existing model"]
    choice = imp.g.choicebox("Choose an action", choices=choices)

    if choice == "Generate Text":
        print("Generating text from a premade model...")
        if imp.torch.cuda.is_available():
            device = imp.torch.device('cuda')
        else:
            device = imp.torch.device('cpu')

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

if __name__ == '__main__':
    
    main()
    
