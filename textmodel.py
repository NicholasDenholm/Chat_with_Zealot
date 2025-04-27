import torch.nn as nn
import all_imports as imp

class TextModel(nn.Module):
    def __init__(self, vocab_size, hidden_size, sequence_length):
        super(TextModel, self).__init__()
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        
        # Define the layers
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size) # fully connected layer
        
        
        #self.rnn = nn.LSTM(hidden_size, hidden_size) # LSTM layer
    
    def forward(self, input, hidden=None):
        # If no hidden state is provided, initialize it
        if hidden is None:
            # (num_layers * num_directions, batch_size, hidden_size)
            hidden = (imp.torch.zeros(1, input.size(0), self.hidden_size).to(input.device),
                      imp.torch.zeros(1, input.size(0), self.hidden_size).to(input.device))

        # Embedding layer
        embedded = self.embedding(input)  # (batch_size, seq_len, hidden_size)

        # Pass through LSTM
        output, hidden = self.lstm(embedded, hidden)  # (batch_size, seq_len, hidden_size), (h, c)

        # Apply the final fully connected layer
        output = self.fc(output)  # (batch_size, seq_len, vocab_size)

        return output, hidden

    def forward_test(self, x):
        embedded = self.embedding(x)  # Shape: (batch_size, seq_len, hidden_size)
        lstm_out, (hn, cn) = self.lstm(embedded)
        output = self.fc(lstm_out)  # Shape: (batch_size, seq_len, vocab_size)
        return output