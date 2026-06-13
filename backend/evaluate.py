import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# UPDATED IMPORTS FOR MULTI-LABEL
from sklearn.metrics import accuracy_score, classification_report, multilabel_confusion_matrix
from sklearn.calibration import calibration_curve

def evaluate_model():
    print("Loading Multi-Label Intelligent Model from ./saved_model...")
    
    # 1. Load your custom trained model
    model_path = "./saved_model"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    model.eval() # Set to evaluation mode
    
    # 2. Load Validation Data (JSON to preserve arrays)
    print("Loading validation dataset (val.json)...")
    val_df = pd.read_json("val.json", lines=True)
    
    texts = val_df["code"].tolist()
    true_labels = val_df["labels"].tolist() # This is now a list of arrays!
    
    print(f"Running inference on {len(texts)} samples. This might take a moment...")
    
    predictions = []
    confidences = []
    
    with torch.no_grad():
        for text in texts:
            # Tokenize
            inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            # Forward pass
            outputs = model(**inputs)
            logits = outputs.logits
            
            # MULTI-LABEL MATH: Apply Sigmoid to get independent probabilities
            probs = torch.sigmoid(logits).squeeze()
            
            # Apply 0.5 threshold to get binary predictions [0, 1, 0, 1, 1, 0]
            predicted_classes = (probs > 0.5).int().tolist()
            
            predictions.append(predicted_classes)
            confidences.append(probs.tolist()) # Save raw probabilities for the calibration curve

    # 4. Calculate Core Metrics
    # In Multi-Label, Exact Match Accuracy is very strict (every single label must be right)
    exact_match_acc = accuracy_score(true_labels, predictions)
    print("\n" + "="*50)
    print(f" EXACT MATCH ACCURACY: {exact_match_acc * 100:.2f}%")
    print("="*50)
    print("\nDetailed Multi-Label Classification Report:")
    
    # Our new 6 OWASP Classes
    #target_names = ['Benign', 'RCE', 'FileOps', 'Exfil', 'Obf', 'Persistent']
    target_names = ['Benign', 'RCE', 'Exfiltration', 'ReverseShell', 'Persistence', 'FileOps']
    print(classification_report(true_labels, predictions, target_names=target_names, zero_division=0))

    # 5. Generate Multi-Label Confusion Matrix Grid (Thesis Figure 1)
    print("\nGenerating Multi-Label Confusion Matrices...")
    mcm = multilabel_confusion_matrix(true_labels, predictions)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.ravel()
    
    for i, (matrix, name) in enumerate(zip(mcm, target_names)):
        sns.heatmap(matrix, annot=True, fmt='d', cmap='Blues', ax=axes[i], cbar=False,
                    xticklabels=['False', 'True'], yticklabels=['False', 'True'])
        axes[i].set_title(f'Class: {name}', fontsize=14, weight='bold')
        axes[i].set_ylabel('Actual', fontsize=12)
        axes[i].set_xlabel('Predicted', fontsize=12)
        
    plt.suptitle('CodeBERT Multi-Label Confusion Matrices', fontsize=18, weight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig('thesis_confusion_matrix.png', bbox_inches='tight', dpi=300)
    print("-> Saved 'thesis_confusion_matrix.png' (It is now a 6-grid image!)")

    # 6. Generate Reliability Diagram for RQ2 (Thesis Figure 2)
    print("Generating Calibration/Reliability Diagram (RQ2)...")
    
    # Flatten the arrays to calculate overall model calibration across all classes
    y_true_flat = np.array(true_labels).flatten()
    y_prob_flat = np.array(confidences).flatten()
    
    prob_true, prob_pred = calibration_curve(y_true_flat, y_prob_flat, n_bins=10)
    
    plt.figure(figsize=(8, 8))
    plt.plot([0, 1], [0, 1], linestyle='--', label='Perfectly Calibrated (Ideal)', color='gray')
    plt.plot(prob_pred, prob_true, marker='o', label='CodeBERT Confidence', color='blue', linewidth=2)
    plt.title('Overall Reliability Diagram (Calibration Curve)', fontsize=14, weight='bold')
    plt.xlabel('Mean Predicted Probability (Confidence)', fontsize=12)
    plt.ylabel('Fraction of True Positives (Accuracy)', fontsize=12)
    plt.legend(loc='lower right', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('thesis_reliability_diagram.png', dpi=300)
    print("-> Saved 'thesis_reliability_diagram.png'")
    print("\nEvaluation Complete! Check your folder for the new PNG charts.")

if __name__ == "__main__":
    evaluate_model()