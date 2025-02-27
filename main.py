import os
import torch

# Assuming this is the function for loading your book text (define it if needed)
def load_data(file_path):
    # Example: Load file text (Replace with actual logic)
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():

    #text = os.startfile("C\\Users\\")
    file_path = os.startfile('explorer')
    
    text = load_data(file_path) # Replace_file_path
        
    data = [1,2,3,4,5,6]

    tensor = torch.tensor(data)

    print((tensor))

    print((tensor.shape))


    x = torch.rand(5, 3)
    print(x)

    print("Hello")


if __name__ == '__main__':
    main()