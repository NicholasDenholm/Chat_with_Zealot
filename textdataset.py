from torch.utils.data import Dataset

class TextDataset(Dataset):

    def __init__(self, text, sequence_length):
        self.text = text
        self.sequence_length = sequence_length
        self.vocab = sorted(set(text))  # Vocabulary
        self.char_to_idx = {char: idx for idx, char in enumerate(self.vocab)}
        self.idx_to_char = {idx: char for idx, char in enumerate(self.vocab)}
        self.data = self.create_sequences()

    def create_sequences(self):
        sequences = []
        targets = []
        for i in range(len(self.text) - self.sequence_length):
            sequences.append(self.text[i:i + self.sequence_length])
            targets.append(self.text[i + 1:i + self.sequence_length + 1])  # next character is the target
        return list(zip(sequences, targets))

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sequence, target = self.data[idx]
        sequence_idx = torch.tensor([self.char_to_idx[char] for char in sequence], dtype=torch.long)
        target_idx = torch.tensor([self.char_to_idx[char] for char in target], dtype=torch.long)
        return sequence_idx, target_idx