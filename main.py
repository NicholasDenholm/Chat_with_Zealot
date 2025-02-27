import os
import torch
from test import Testing
from textdataset import TextDataset
from loading import Loading

def main():

    # Hyperparameters
    batch_size = 64
    sequence_length = 100
    hidden_size = 256
    num_epochs = 20
    learning_rate = 0.001

    
    file_path = os.startfile('explorer')
    text = load_data(file_path) # Replace_file_path

    dataset = TextDataset(text, sequence_length)
        
    
    print("Hello")


if __name__ == '__main__':
    main()