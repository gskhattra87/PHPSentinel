import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from transformers import RobertaTokenizer, RobertaForSequenceClassification

# 1. Load model and tokenizer
model_path = "microsoft/codebert-base" 
tokenizer = RobertaTokenizer.from_pretrained(model_path)
model = RobertaForSequenceClassification.from_pretrained(model_path, output_attentions=True)
model.eval()

# 2. PHP Code
php_code = """<?php 
$auth = $_COOKIE['session'];
if($auth === "admin"){
    $cmd = $_POST['execute'];
    system($cmd);
}
?>"""

# 3. Tokenize
inputs = tokenizer(php_code, return_tensors="pt", add_special_tokens=True)
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])

# 4. Extract Attention
with torch.no_grad():
    outputs = model(**inputs)

last_layer_attention = outputs.attentions[-1]
avg_attention = torch.mean(last_layer_attention[0], dim=0).numpy()
cls_attention = avg_attention[0, :]

# 5. Clean Data & WHITESPACE PRUNING
tokens = tokens[1:-1]
cls_attention = cls_attention[1:-1]

clean_tokens = []
valid_indices = [] # Tracks the indices of the actual code tokens

for i, t in enumerate(tokens):
    t = t.replace('Ċ', '[NL]')  
    t = t.replace('Ġ', '')      
    if t == '':
        t = '[INDENT]'
        
    # THE FIX: Only keep the token if it is NOT whitespace or a newline
    if t not in ['[NL]', '[INDENT]']:
        clean_tokens.append(t)
        valid_indices.append(i)

# Filter the attention weights to perfectly match the pruned tokens
cls_attention = cls_attention[valid_indices]


# --- BRUTE-FORCE PLOTTING ---

# Dynamic Height Calculation (Slightly more compressed since we removed the junk tokens)
fig_height = max(8, len(clean_tokens) * 0.4) 
fig, ax = plt.subplots(figsize=(9, fig_height))

# Color mapping
norm = Normalize(vmin=0, vmax=np.percentile(cls_attention, 95))
cmap = plt.get_cmap("Reds")
colors = cmap(norm(cls_attention))

y_positions = np.arange(len(clean_tokens))
bars = ax.barh(y_positions, cls_attention, color=colors, edgecolor='black', linewidth=0.5)
ax.invert_yaxis()

# Y-Axis Labels
ax.set_yticks(y_positions)
ax.set_yticklabels(clean_tokens, fontfamily='monospace', fontsize=11)

# X-Axis Labels
ax.set_xlabel("Relative Semantic Weight (Attention)", fontsize=14, fontweight='bold', labelpad=15)
ax.xaxis.grid(True, linestyle='--', alpha=0.6)
ax.set_axisbelow(True)

# Colorbar
sm = ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, aspect=40, pad=0.03)
cbar.set_label('Attention Intensity', fontsize=12, labelpad=15)

# Standard title placement 
plt.title("CodeBERT Semantic Focus\n(RCE Webshell Analysis)", fontsize=18, fontweight='bold')

# Absolute Manual Margins
plt.subplots_adjust(left=0.20, right=0.95, top=0.91, bottom=0.08)

# Save the file
plt.savefig("attention_vertical_profile_rce_PRUNED.png", dpi=300, facecolor='white')
plt.show()