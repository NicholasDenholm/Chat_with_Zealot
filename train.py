import torch
import torch.optim as optim
from torch.cuda.amp import GradScaler, autocast
from tqdm import tqdm

class Train:

    @staticmethod
    def train(model, dataloader, criterion, optimizer, num_epochs, device, accumulation_steps=4):
        scaler = torch.amp.GradScaler(f"{device}")  # For mixed precision training

        for epoch in range(num_epochs):
            model.train()
            total_loss = 0
            
            # If multiple GPUs available, use DataParallel
            if torch.cuda.device_count() > 1:
                model = torch.nn.DataParallel(model)
            model.to(device)

            # Wrap the dataloader with tqdm to show a progress bar
            # tqdm(dataloader) automatically calculates the number of batches and shows the progress
            epoch_progress = tqdm(dataloader, desc=f'Epoch {epoch+1}/{num_epochs}', dynamic_ncols=True)
            
            
            for step, (input_seq, target_seq) in enumerate(epoch_progress):


                # Move to device used, either CPU or GPU
                input_seq, target_seq = input_seq.to(device), target_seq.to(device) 

                optimizer.zero_grad()

                with autocast():  # Mixed precision
                    output = model(input_seq)
                    output = output.view(-1, output.size(-1))
                    target_seq = target_seq.view(-1)
                    loss = criterion(output, target_seq)

                scaler.scale(loss).backward()

                # Accumulate gradients every `accumulation_steps` mini-batches
                if (step + 1) % accumulation_steps == 0:
                    scaler.step(optimizer)
                    scaler.update()

                total_loss += loss.item()

                # Update progress bar with current loss
                epoch_progress.set_postfix(loss=total_loss / (step + 1))
            
            print(f'Epoch {epoch+1}/{num_epochs}, Loss: {total_loss / len(dataloader)}')
        
        print("Model done training!")