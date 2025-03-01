import all_imports as imp

def main():

    # Hyperparameters
    batch_size = 64
    sequence_length = 100
    hidden_size = 256
    num_epochs = 20
    learning_rate = 0.001

    print("Hello")
    
    load_inst = imp.Loading()
    file_path = load_inst.load_data_box()
    print(f"Data from: {file_path} was loaded")

    text = load_inst.load_n_process_data()

    dataset = imp.TextDataset(text, sequence_length)

    print(len(text))  # Check if the dataset has samples


    dataloader = imp.torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    
    # Is this correct?
    vocab_size = len(dataset)
    
    model = imp.TextModel(vocab_size, hidden_size, sequence_length)
    
    criterion = imp.nn.CrossEntropyLoss()
    optimizer = imp.optim.Adam(model.parameters(), lr=learning_rate)
    
    imp.Train.train(model, dataloader, criterion, optimizer, num_epochs)
    #trainee = imp.Train()
    #trainee.train(model, dataloader, criterion, optimizer, num_epochs)

    
    # Get the current date to append to the filename so overwrites dont happen
    # Format as YYYY-MM-DD_Hour-Min-Second
    current_date = imp.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
    output_path = load_inst.set_output_folder()
    model_save_path = imp.os.path.join(output_path, f'text_model_{current_date}.pth')
    # After training, save the model
    imp.torch.save(model.state_dict(), model_save_path)
    

    # Generate text after training
    generator = imp.Generate_Text()
    seed_text = "Once upon a time"
    generated_text = generator.generate_text(model, seed_text, sequence_length, 500, dataset.char_to_idx, dataset.idx_to_char)
    print(generated_text)

    # Load the model and generate text
    loaded_model = imp.TextModel(vocab_size, hidden_size=256, sequence_length=sequence_length)
    loaded_model.load_state_dict(imp.torch.load('text_model.pth'))
    loaded_model.eval()
    
    # Generate text from the loaded model
    generated_text = generator.generate_text(loaded_model, seed_text, sequence_length, 500, dataset.char_to_idx, dataset.idx_to_char)
    print(generated_text)


if __name__ == '__main__':
    main()