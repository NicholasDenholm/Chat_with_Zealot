import torch.optim as optim

class Train:

    @staticmethod
    def train(model, dataloader, criterion, optimizer, num_epochs):
        for epoch in range(num_epochs):
            model.train()
            total_loss = 0
            for input_seq, target_seq in dataloader:
                optimizer.zero_grad()
                
                output = model(input_seq)
                
                # Reshape output and target to [batch_size * sequence_length, vocab_size]
                output = output.view(-1, output.size(-1))
                target_seq = target_seq.view(-1)
                
                loss = criterion(output, target_seq)
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            print(f'Epoch {epoch+1}/{num_epochs}, Loss: {total_loss / len(dataloader)}')
        
        print("Model done training!")