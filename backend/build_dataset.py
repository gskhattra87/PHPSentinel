import os
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from deobfuscator import PHPDeobfuscator

# Define the 6 OWASP Classes
# CLASSES = ['Benign', 'RCE', 'FileOps', 'Exfil', 'Obf', 'Persistent']
CLASSES = ['Benign', 'RCE', 'Exfiltration', 'ReverseShell', 'Persistence', 'FileOps']

# Regex patterns to automatically detect secondary behaviors in malicious files

KEYWORD_PATTERNS = {
    1: r"(system|shell_exec|exec|passthru|popen|proc_open)\s*\(",  # 1_RCE
    2: r"(mysql_query|mysqli_query|PDO|UNION\s+SELECT|wget|curl)\s*\(?", # 2_Exfiltration
    3: r"(fsockopen|nc\s+-e|bash\s+-i|/dev/tcp/|base64_decode|eval)\s*\(?", # 3_ReverseShell
    4: r"(crontab|schtasks|auto_prepend_file|register_shutdown_function)", # 4_Persistence
    5: r"(fopen|chmod|unlink|rename|file_put_contents|rmdir)\s*\("  # 5_FileOps
}

def build_dataset(root_folder="dataset_raw"):
    print(f"Scanning directory: {root_folder} recursively for Multi-Label mapping...")
    data = []
    
    # Map folder prefixes to their Primary Index
    label_mapping = {
        "0_": 0, "1_": 1, "2_": 2, 
        "3_": 3, "4_": 4, "5_": 5
    }

    if not os.path.exists(root_folder):
        print(f" Error: Could not find the folder '{root_folder}'.")
        return

    for folder_name in os.listdir(root_folder):
        label_folder_path = os.path.join(root_folder, folder_name)
        if not os.path.isdir(label_folder_path):
            continue
            
        primary_idx = None
        for prefix, lbl in label_mapping.items():
            if folder_name.startswith(prefix):
                primary_idx = lbl
                break
                
        if primary_idx is None:
            continue
            
        print(f"Scanning '{folder_name}'...")
        file_count = 0
        
        for current_dir, _, files in os.walk(label_folder_path):
            for file in files:
                if file.endswith(".php") or file.endswith(".txt"):
                    file_path = os.path.join(current_dir, file)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            raw_content = f.read().strip()
                            
                            if raw_content:
                                # 1. Initialize empty 6-element binary array [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                                label_vector = [0.0] * 6
                                
                                # 2. Always set the primary label based on the folder it was found in
                                label_vector[primary_idx] = 1.0
                                
                                # 3. Auto-Tagging: If it's malicious, scan for other behaviors!
                                if primary_idx != 0:
                                    for class_idx, pattern in KEYWORD_PATTERNS.items():
                                        if re.search(pattern, raw_content, re.IGNORECASE):
                                            label_vector[class_idx] = 1.0
                                
                                # 4. Clean the code for the AI
                                cleaner = PHPDeobfuscator()
                                clean_content = cleaner.clean(raw_content)
                                
                                # Save data. We keep 'primary_idx' temporarily for safe stratifying.
                                data.append({
                                    "code": clean_content, 
                                    "labels": label_vector, 
                                    "primary_label": primary_idx
                                })
                                file_count += 1
                    except Exception:
                        pass
                        
        print(f" Loaded {file_count} files for Folder Prefix {primary_idx}")

    if not data:
        print(" No valid PHP files found!")
        return
        
    df = pd.DataFrame(data)
    print(f"\nTotal Dataset Size: {len(df)} scripts")

    # Split into 80% Training, 20% Validation (Stratified by primary folder to keep math balanced)
    print("Splitting into Training and Validation sets...")
    train_df, val_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["primary_label"])

    # Drop the temporary 'primary_label' column, we only need the array now
    train_df = train_df.drop(columns=["primary_label"])
    val_df = val_df.drop(columns=["primary_label"])

    # Save to JSON format instead of CSV. 
    # CSVs convert lists into ugly strings. JSON natively supports arrays!
    train_df.to_json("train.json", orient="records", lines=True)
    val_df.to_json("val.json", orient="records", lines=True)
    
    print("\n SUCCESS! Generated 'train.json' and 'val.json' with Multi-Label Arrays.")
    print("Example label format: [0.0, 1.0, 0.0, 0.0, 1.0, 0.0]")

if __name__ == "__main__":
    build_dataset()