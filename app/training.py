import torch
from torch.utils.data import Dataset, DataLoader
from pytorch_lightning import LightningModule, Trainer
from pytorch_lightning.callbacks import ModelCheckpoint

class JourneyDataset(Dataset):
    def __init__(self, data_dir):
        self.data = load_training_data(data_dir)
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]

class PLJourneyModel(LightningModule):
    def __init__(self):
        super().__init__()
        self.model = EnhancedJourneyModel()
        self.criterion = nn.CrossEntropyLoss()
        
    def training_step(self, batch, batch_idx):
        frames, labels = batch
        outputs = self.model(frames)
        loss = self.criterion(outputs['events'], labels)
        self.log('train_loss', loss)
        return loss
    
    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=1e-4)
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, patience=3, factor=0.5
        )
        return {
            'optimizer': optimizer,
            'lr_scheduler': scheduler,
            'monitor': 'train_loss'
        }

def train_new_model():
    # Create dataset from training data
    dataset = JourneyDataset('data/training_data')
    loader = DataLoader(dataset, batch_size=32, shuffle=True)
    
    # Initialize model
    model = PLJourneyModel()
    
    # Configure training
    checkpoint_callback = ModelCheckpoint(
        dirpath='models',
        filename='best-{epoch:02d}-{val_loss:.2f}',
        save_top_k=1,
        monitor='val_loss'
    )
    
    trainer = Trainer(
        gpus=1,
        max_epochs=20,
        callbacks=[checkpoint_callback],
        precision=16  # Mixed precision training
    )
    
    # Train and validate
    trainer.fit(model, loader)
    
    # Save final model
    torch.save(model.state_dict(), 'models/latest.pt')