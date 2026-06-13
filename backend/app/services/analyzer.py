import torch
import re
import asyncio
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.logic.risk_manager import selective_prediction

class MalwareAnalyzer:
    """
    Core engine for PHPSentinel. 
    Uses CodeBERT to analyze intent and classify malware behaviors.
    Includes Semantic Highlighting and Normalization logic.
    """
    def __init__(self):
        # Initializing CodeBERT from your custom fine-tuned weights
        self.tokenizer = AutoTokenizer.from_pretrained("./saved_model")
        self.model = AutoModelForSequenceClassification.from_pretrained(
            "./saved_model", 
            num_labels=6, 
            ignore_mismatched_sizes=True
        )
        # Set to evaluation mode to disable dropout layers
        self.model.eval() 

    async def analyze_code(self, raw_code: str):
        # 1. Normalization: Peeling back obfuscation layers
        normalized_code = self.preprocess(raw_code)
       
        # 2. Transformer Pass: Contextual embedding extraction
        inputs = self.tokenizer(
            normalized_code, 
            return_tensors="pt", 
            truncation=True, 
            max_length=512
        )
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # 3. Probability Calculation (CRITICAL FIX: Sigmoid for Multi-Label)
        # Squeeze removes the batch dimension so we get a 1D tensor of 6 probabilities
        probs = torch.sigmoid(outputs.logits).squeeze()
        
        # Mapping logits to our behavioral taxonomy
        current_risk_profile = {
            "Benign": probs[0].item(),
            "RCE": probs[1].item(),
            "Exfiltration": probs[2].item(),
            "ReverseShell": probs[3].item(),
            "Persistence": probs[4].item(),
            "FileManipulation": probs[5].item()
        }
        
        # We only want to evaluate the 'confidence' of a threat based on malicious categories.
        # Otherwise, a 99% confident Benign file would trigger the RiskManager to block it!
        malicious_probs = [
            current_risk_profile["RCE"],
            current_risk_profile["Exfiltration"],
            current_risk_profile["ReverseShell"],
            current_risk_profile["Persistence"],
            current_risk_profile["FileManipulation"]
        ]
        
        # Threat confidence is the highest probability among malicious classes
        threat_confidence = max(malicious_probs) if malicious_probs else 0.0
        
        # 4. Selective Prediction & Decision Engine (RQ5)
        decision_data = selective_prediction(threat_confidence, current_risk_profile)

        # 5. Semantic Evidence Extraction (For Highlighting in UI)
        evidence = await self.get_semantic_evidence(normalized_code, current_risk_profile)

        return {
            "malicious_score": sum(malicious_probs), # Cumulative risk
            "risk_profile": current_risk_profile,
            "decision_engine": decision_data,
            "confidence": threat_confidence,
            "original_code": raw_code,          # Required for Frontend Toggle
            "normalized_code": normalized_code, # Required for Frontend Toggle
            "evidence": evidence,               # Required for Semantic Highlighting
            "metadata": {
                "model": "CodeBERT-base",
                "tokens": inputs['input_ids'].shape[1]
            }
        }

    async def get_semantic_evidence(self, code: str, risk_profile: dict):
        """
        Identifies specific lines that contribute to the risk score.
        Acts as an explainability (XAI) layer for the Transformer.
        """
        evidence = []
        lines = code.split('\n')
        
        # Patterns correlated with the behavioral head categories
        patterns = {
            "RCE": [r"eval\(", r"assert\(", r"base64_decode", r"shell_exec", r"system\("],
            "ReverseShell": [r"fsockopen", r"pfsockopen", r"/bin/bash", r"tcp://"],
            "Persistence": [r"\.htaccess", r"auto_prepend_file", r"crontab"],
            "Exfiltration": [r"curl_exec", r"ftp_put", r"wp-config\.php", r"mysql_query"],
            "FileManipulation": [r"fopen\(", r"fwrite\(", r"unlink\(", r"file_put_contents\("]
        }

        for i, line in enumerate(lines):
            for intent, regex_list in patterns.items():
                # Only look for evidence if the model found a high probability for this intent
                if risk_profile.get(intent, 0) > 0.3: 
                    for pattern in regex_list:
                        if re.search(pattern, line, re.IGNORECASE):
                            evidence.append({
                                "line": i + 1,
                                "intent": intent,
                                "content": line.strip()
                            })
        return evidence

    def preprocess(self, code: str):
        """
        Deobfuscation Pipeline: Strips noise and normalizes structure.
        Addresses RQ1 regarding static analysis limitations.
        """
        if not code or not isinstance(code, str):
            return ""
            
        # Basic cleanup
        code = code.replace("<?php", "").replace("?>", "")
        # Remove comments (Multi-line and Single-line)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL) 
        code = re.sub(r'//.*', '', code) 
        code = re.sub(r'#.*', '', code)
        # Standardize whitespace for transformer tokenization
        return "\n".join([line.strip() for line in code.splitlines() if line.strip()])