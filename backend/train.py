import torch
import numpy as np
import pandas as pd
from sklearn.metrics import f1_score
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from torch.utils.data import DataLoader
from torch.optim import AdamW

# --- 1. OUR CUSTOM DATASET ---
class PHPMalwareDataset(torch.utils.data.Dataset):
    def __init__(self, dataframe, tokenizer, max_length=512):
        self.texts = dataframe["code"].tolist()
        self.labels = dataframe["labels"].tolist()
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label_tensor = torch.tensor([float(l) for l in self.labels[idx]], dtype=torch.float)
        
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_length,
            return_tensors='pt'
        )
        
        item = {key: val.squeeze(0) for key, val in encoding.items()}
        item['labels'] = label_tensor
        return item

# --- 2. PURE PYTORCH TRAINING LOOP ---
def train_model():
    # Detect if you have a GPU, otherwise fallback to CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"🚀 Initializing compute on: {device}")

    # Load Model & Tokenizer
    model_name = "microsoft/codebert-base"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name, 
        num_labels=6,
        problem_type="multi_label_classification",
        ignore_mismatched_sizes=True
    )
    model.to(device) # Move model to GPU/CPU

    print("📂 Loading JSON data...")
    train_df = pd.read_json("train.json", lines=True)
    val_df = pd.read_json("val.json", lines=True)

    # Initialize PyTorch DataLoaders (Batch size of 8)
    train_dataset = PHPMalwareDataset(train_df, tokenizer)
    val_dataset = PHPMalwareDataset(val_df, tokenizer)
    
    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=8)

    # Initialize standard AdamW Optimizer
    optimizer = AdamW(model.parameters(), lr=2e-5)
    epochs = 5

    print("\n🔥 Starting Pure PyTorch Training (Bypassing Windows Security Block)...")

    for epoch in range(epochs):
        print(f"\n--- Epoch {epoch + 1}/{epochs} ---")
        
        # --- TRAINING PHASE ---
        model.train()
        total_train_loss = 0

        for step, batch in enumerate(train_loader):
            # Move data to GPU/CPU
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            # Forward pass
            model.zero_grad()
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            
            # Hugging Face models calculate BCE loss automatically if labels are provided!
            loss = outputs.loss
            total_train_loss += loss.item()

            # Backward pass (learn!)
            loss.backward()
            optimizer.step()

            # Print progress every 50 batches
            if step % 50 == 0 and step > 0:
                print(f"  Step {step}/{len(train_loader)} | Current Loss: {loss.item():.4f}")

        avg_train_loss = total_train_loss / len(train_loader)
        print(f"✅ Epoch {epoch + 1} Training Loss: {avg_train_loss:.4f}")

        # --- VALIDATION PHASE ---
        model.eval()
        print("🔍 Running Validation...")
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)

                outputs = model(input_ids=input_ids, attention_mask=attention_mask)
                
                # Apply Sigmoid mathematically to get probabilities
                probs = torch.sigmoid(outputs.logits).cpu().numpy()
                
                # Convert to binary predictions
                preds = (probs > 0.5).astype(int)

                all_preds.extend(preds)
                all_labels.extend(labels.cpu().numpy())

        # Calculate Macro F1 Score for this epoch
        macro_f1 = f1_score(all_labels, all_preds, average="macro", zero_division=0)
        print(f"🎯 Epoch {epoch + 1} Validation Macro F1 Score: {macro_f1:.4f}")

    # --- SAVE THE MODEL ---
    print("\n💾 Saving highly-trained model...")
    model.save_pretrained("./saved_model")
    tokenizer.save_pretrained("./saved_model")
    print("🎉 Training complete! Multi-Label Model saved to ./saved_model")

if __name__ == "__main__":
    train_model()