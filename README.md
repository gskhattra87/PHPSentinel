# PHPSentinel: Multi-Label Obfuscated PHP Malware Detection

This repository contains the complete source code and structural framework for **PHPSentinel**, a hybrid security engine I engineered for my Master's thesis. The system bridges the gap between rigid signature scanners and deep learning models by combining a static, deterministic source-code deobfuscator with a bimodal Transformer network (fine-tuned CodeBERT) to perform multi-label behavioral classification on server-side PHP scripts.

Traditional tools often miss threats when attackers use complex variable fragmentation or layered encoding wrappers. PHPSentinel solves this by peeling back those obfuscation layers statically before piping clean code tokens into an attention-based AI network.

---

## 🏗️ System Architecture

The execution pipeline operates across three major decoupling phases:

1. **AST-Based Deobfuscator (`deobfuscator.py`):** A custom Python filter that hooks into raw syntax structures, strips out junk developer comments, flattens line spacing, and statically decodes nested Base64 or hexadecimal layers without ever executing the untrusted file.
2. **Transformer Inference Engine (`model/`):** A fine-tuned, 125-million parameter bimodal CodeBERT network that reads the unpacked token sequences, computes global self-attention mappings, and outputs a joint probability distribution across six distinct behavioral target classes.
3. **Enterprise Monitoring Layer (`api/` & `dashboard/`):** A lightweight FastAPI server backend that processes incoming scripts on the fly, linked directly to an interactive React frontend telemetry dashboard for system administrators.

---

## 📁 Repository Structure

```text
PHPSentinel/
├── api/                  # FastAPI backend inference router
│   └── main.py
├── core/                 # Core normalization logic
│   └── deobfuscator.py   # AST-based cleaner and unpacking engine
├── dashboard/            # React administration frontend
├── data/                 # Dataset manifests and curation maps
│   └── dataset_manifest.csv
├── model/                # Model evaluation loops and weight configs
│   ├── train.py
│   └── evaluate.py
├── requirements.txt      # Python system dependencies
└── README.md


## 🚀 Quick Start & Installation
Prerequisite Environment
Make sure your system has Python 3.10+ and a local PHP CLI binary installed (used strictly by the linting sanity checks during code parsing).
# Clone the repository
git clone [https://github.com/gskhattra87/PHPSentinel.git](https://github.com/gskhattra87/PHPSentinel.git)
cd PHPSentinel

# Setup a clean virtual environment
python3 -m venv venv
source venv/bin/activate

# Install essential deep learning and processing dependencies
pip install -r requirements.txt


## 💻 Usage
1. Running the Deobfuscator Statically
To run an isolated cleaning test on a suspicious, scrambled script file, feed it directly into the core pre-processing script:

python core/deobfuscator.py --input /path/to/suspect.php --output /path/to/clean_output.txt

2. Spinning Up the Classification API Backend
To start the FastAPI inference worker node to evaluate inbound web payloads:

cd api
uvicorn main:app --host 127.0.0.1 --port 8000 --reload

## 📊 Dataset & Compliance Policy
To comply with GitHub security guidelines and platform distribution regulations regarding malicious code, this repository does not host raw, executable malware binaries. Hosting live webshells or active remote code execution scripts poses a clear risk and violates platform policies.

Instead, I built a reliable tracking system inside the data/ folder:

data/dataset_manifest.csv: This master data card indexes all 5,389 code samples utilized throughout my training loops. Each script entry is safely identified by its unique SHA-256 cryptographic hash, multi-label behavioral array annotations, and its original public source repository link.

Aggregated Sources: The dataset maps clean logic from framework components (Laravel Core and PHP-Parser) against real-world attack payloads gathered from open-access security collections (MWF-Dataset, PHP-Malware-Collection, and the Cyc1e183 PHP-Webshell-Dataset).

If you want to replicate my exact experimental splits (80/10/10), you can execute the provided ingestion helper script to safely fetch, hash-verify, and assemble the training partitions locally on your machine.

## 🎯 Classification Taxonomy
Instead of generating a simple "safe or unsafe" decision, the model calculates independent probability confidence metrics ranging from 0.0 to 1.0 using a Sigmoid activation setup across six target groups simultaneously:

Benign: Safe, standardized administrative applications.

RCE (Remote Code Execution): Inbound string evaluation exploits (eval, assert).

Exfiltration: Unauthorized network data leaks or file uploads.

ReverseShell: Persistent outbound raw socket connections back to an attacker.

Persistence: Automated configuration modifications or system cron injections.

FileOps: Unauthorized storage directory modifications (tracked via explicit file-manipulation rules).


