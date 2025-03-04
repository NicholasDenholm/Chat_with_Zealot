import all_imports as imp

def main():

    batch_size = 4
    sequence_length = 64
    hidden_size = 128
    num_epochs = 3
    learning_rate = 0.001
    

    print("Hello")
    
    load_inst = imp.Loading()
    file_path = load_inst.load_data_box()
    print(f"Data from: {file_path} was loaded")

    text = load_inst.load_n_process_data()

    dataset = imp.TextDataset(text, sequence_length)

    print(len(text))  # Check if the dataset has samples

    dataloader = imp.torch.utils.data.DataLoader(dataset, batch_size=batch_size, num_workers=8, shuffle=True)
    vocab_size = len(dataset)
    
    if imp.torch.cuda.is_available():
        device = imp.torch.device('cuda')
        print(f'CUDA is available. Using device: {imp.torch.cuda.get_device_name(0)}')
    else:
        device = imp.torch.device('cpu')
        print('CUDA is not available. Using CPU.')
    
    # Check if CUDA is available
    #device = imp.torch.device('cuda' if imp.torch.cuda.is_available() else 'cpu')
    #print(f'Using device: {device}')
    
    model = imp.TextModel(vocab_size, hidden_size, sequence_length)
    model = model.to(device)  # Move the model to the correct device (GPU or CPU)


    criterion = imp.nn.CrossEntropyLoss()
    optimizer = imp.optim.Adam(model.parameters(), lr=learning_rate)
    scheduler = imp.torch.optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    
    imp.Train.train(model, dataloader, criterion, optimizer, num_epochs, device)
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
    #generator = imp.Generate_Text()
    seed_text = "Once upon a time"
    num_of_generated_chars = 50 # How many characters to generate
    generated_text = imp.GenerateText.generate_text(model, seed_text, sequence_length, num_of_generated_chars, dataset.char_to_idx, dataset.idx_to_char)
    print(generated_text)


    '''
    # Load the model and generate text
    loaded_model = imp.TextModel(vocab_size, hidden_size=256, sequence_length=sequence_length)
    loaded_model.load_state_dict(imp.torch.load('text_model.pth'))
    loaded_model.eval()
    
    # Generate text from the loaded model
    generated_text = generator.generate_text(loaded_model, seed_text, sequence_length, 500, dataset.char_to_idx, dataset.idx_to_char)
    print(generated_text)
    '''

if __name__ == '__main__':
    
    main()
    
    # Use bottleneck profiling to analyze performance
    # python -m torch.utils.bottleneck your_training_script.py
