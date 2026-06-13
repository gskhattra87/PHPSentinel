# 🛡️ PHPSentinel: AI Malware Intelligence Platform

> **Research Prototype** for semantic detection and behavioral mapping of PHP webshells and obfuscated malware using fine-tuned CodeBERT.

PHPSentinel is a full-stack cybersecurity application developed as a thesis project to explore the efficacy of Large Language Models (LLMs) in identifying malicious intent within PHP scripts. Unlike traditional signature-based antiviruses, PHPSentinel uses a fine-tuned CodeBERT backbone to "read" code semantics, bypassing common obfuscation techniques.

---

## ✨ Key Features & Research Objectives

* **Semantic Deobfuscation (RQ1):** Pre-processing pipeline that normalizes string concatenation, base64 encoding, and variable-variables before inference.
* **Confidence Calibration (RQ2):** Utilizes Temperature Scaling to reduce Expected Calibration Error (ECE), ensuring the "Threat Probability" score represents true statistical risk rather than raw logits.
* **Behavioral Mapping (RQ3):** Multi-label classification head that maps code sequences to 6 specific threat intents (e.g., Remote Code Execution, Exfiltration, Persistence).
* **Explainable AI (XAI):** Real-time semantic highlighting using the Monaco Editor to show security analysts exactly *which* lines of code triggered the AI.
* **Incident Response Ready:** Generates portable, high-fidelity PDF intelligence reports for security teams.

---

## 🏗️ System Architecture

* **Backend:** Python, FastAPI, PyTorch, Hugging Face `transformers`
* **Frontend:** React.js, Tailwind CSS (v3), Lucide Icons, `@monaco-editor/react`
* **AI Engine:** `microsoft/codebert-base` (Fine-tuned for PHP sequence classification)

---

## 🚀 Installation & Setup

You will need two terminal windows to run both the API backend and the React frontend simultaneously. 

### Prerequisites
* Python 3.10+
* Node.js v18+ & npm

### 1. Backend Setup (FastAPI + AI Engine)
Navigate to the root directory and set up the Python environment:
```bash
# Create and activate a virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Navigate to the backend folder
cd backend

# Install dependencies
pip install fastapi uvicorn torch transformers datasets pandas scikit-learn matplotlib seaborn python-multipart

# Start the server
uvicorn main:app --reload --port 8000