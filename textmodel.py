import torch.nn as nn

class TextModel(nn.Module):
    def __init__(self, vocab_size, hidden_size, sequence_length):
        super(TextModel, self).__init__()
        self.hidden_size = hidden_size
        self.sequence_length = sequence_length
        
        # Define the layers
        self.embedding = nn.Embedding(vocab_size, hidden_size)
        self.lstm = nn.LSTM(hidden_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)
    
    def forward(self, x):
        embedded = self.embedding(x)  # Shape: (batch_size, seq_len, hidden_size)
        lstm_out, (hn, cn) = self.lstm(embedded)
        output = self.fc(lstm_out)  # Shape: (batch_size, seq_len, vocab_size)
        return output