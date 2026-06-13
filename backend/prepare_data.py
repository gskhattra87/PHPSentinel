import os
import pandas as pd
from sklearn.model_selection import train_test_split

def prepare_malware_dataset(data_path):
    """
    Scans directories of PHP files and creates a labeled CSV for training.
    Assumes folder structure: /dataset/RCE/, /dataset/Benign/, etc.
    """
    data = []
    categories = ["Benign", "RCE", "Exfiltration", "ReverseShell", "Persistence", "FileManipulation"]
    
    for label, category in enumerate(categories):
        cat_path = os.path.join(data_path, category)
        if not os.path.exists(cat_path): continue
        
        for file in os.listdir(cat_path):
            if file.endswith(".php"):
                with open(os.path.join(cat_path, file), 'r', errors='ignore') as f:
                    code = f.read()
                    data.append({"code": code, "label": label})
    
    df = pd.DataFrame(data)
    train, val = train_test_split(df, test_size=0.1, stratify=df['label'])
    
    train.to_csv("train.csv", index=False)
    val.to_csv("val.csv", index=False)
    print(f"Dataset prepared: {len(train)} training samples, {len(val)} validation samples.")

if __name__ == "__main__":
    # Create the folder structure first, then run this
    prepare_malware_dataset("./data")