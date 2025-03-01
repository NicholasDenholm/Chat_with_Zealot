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

    dataset = imp.TextDataset(file_path, sequence_length)



    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)
    vocab_size = len(dataset.chars)
    
    model = TextModel(vocab_size, hidden_size, sequence_length)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    train(model, dataloader, criterion, optimizer, num_epochs)

    
    # Get the current date to append to the filename so overwrites dont happen
    # Format as YYYY-MM-DD_Hour-Min-Second
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  
    output_path = load_inst.set_output_folder()
    model_save_path = os.path.join(output_path, f'text_model_{current_date}.pth')
    # After training, save the model
    torch.save(model.state_dict(), model_save_path)
    

    # Generate text after training
    seed_text = "Once upon a time"
    generated_text = generate_text(model, seed_text, sequence_length, 500, dataset.char_to_idx, dataset.idx_to_char)
    print(generated_text)

    # Load the model and generate text
    loaded_model = TextModel(vocab_size, hidden_size=256, sequence_length=sequence_length)
    loaded_model.load_state_dict(torch.load('text_model.pth'))
    loaded_model.eval()
    


if __name__ == '__main__':
    main()