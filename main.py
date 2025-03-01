import all_imports as imp

def main():

    # Hyperparameters
    batch_size = 64
    sequence_length = 100
    hidden_size = 256
    num_epochs = 20
    learning_rate = 0.001

    
    file_path = imp.os.startfile('explorer')
    text = imp.load_data(file_path) # Replace_file_path

    dataset = imp.TextDataset(text, sequence_length)
        
    
    print("Hello")


if __name__ == '__main__':
    main()