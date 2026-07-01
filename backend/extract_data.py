import os
import zipfile
from pathlib import Path

ZIP_DIR = Path("dataset_raw/zip_files")
EXTRACT_DIR = Path("dataset_raw/extracted")

def setup_directories():
    """Ensures the required directories exist."""
    if not ZIP_DIR.exists():
        print(f"Error: Cannot find {ZIP_DIR}.")
        return False
        
    EXTRACT_DIR.mkdir(parents=True, exist_ok=True)
    print(f" Checked directories: \nSource: {ZIP_DIR} \nDestination: {EXTRACT_DIR}")
    return True

def extract_all_zips():
    """Finds all .zip files in the zip_files folder and extracts them."""
    zip_files = list(ZIP_DIR.glob("*.zip"))
    
    if not zip_files:
        print(" No .zip files found in the directory.")
        return

    print(f"\n Found {len(zip_files)} dataset(s). Starting extraction...\n" + "-"*40)
    
    for zip_path in zip_files:
        # Create a specific sub-folder for this zip file's contents
        dataset_name = zip_path.stem
        target_folder = EXTRACT_DIR / dataset_name
        
        # Skip if already extracted
        if target_folder.exists() and any(target_folder.iterdir()):
            print(f"  Skipping: {zip_path.name} (Already extracted)")
            continue
            
        target_folder.mkdir(exist_ok=True)
        print(f" Extracting: {zip_path.name}  -->  {target_folder.name}/")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(target_folder)
        except zipfile.BadZipFile:
            print(f" Error: {zip_path.name} is corrupted or not a valid zip file.")

    print("-" * 40 + "\n All datasets extracted successfully to 'dataset_raw/extracted/'!")

if __name__ == "__main__":
    if setup_directories():
        extract_all_zips()
