from typing import Dict, Any

class RiskManager:
    """
    Implements Risk-Aware Selective Blocking and Uncertainty Logic.
    Based on Thesis Research Question 5 (RQ5) regarding calibrated 
    malware metrics in server decision pipelines.
    """
    
    def __init__(self, high_confidence_threshold: float = 0.85, caution_threshold: float = 0.60):
        # Thresholds to determine 'Coverage' vs 'Selective Deferral'
        self.high_confidence_threshold = high_confidence_threshold
        self.caution_threshold = caution_threshold

    def evaluate_risk(self, confidence_score: float, risk_profile: Dict[str, float]) -> Dict[str, Any]:
        """
        Processes model outputs to determine the final system action.
        Addresses RQ2: Improvement of class confidence calibration.
        """
        
        # 1. Determine Epistemic Uncertainty Status
        # High uncertainty occurs when the model is not confident in its prediction
        if confidence_score < self.caution_threshold:
            uncertainty_status = "High (Epistemic)"
            decision = "Manual Review Required"
            action_code = "DEFER"
        elif confidence_score < self.high_confidence_threshold:
            uncertainty_status = "Moderate"
            decision = "Caution: Probable Malware"
            action_code = "WARN"
        else:
            uncertainty_status = "Low (Confident)"
            decision = "Automatic Action"
            action_code = "BLOCK"

        # 2. Extract the primary threat behavior from the Risk Profile
        # This addresses RQ3: Mapping code sequences to functional behaviors
        primary_intent = max(risk_profile, key=risk_profile.get)
        intent_score = risk_profile[primary_intent]

        return {
            "decision": decision,
            "action_code": action_code,
            "uncertainty_status": uncertainty_status,
            "reliability_metrics": {
                "confidence_score": round(confidence_score, 4),
                "threshold_applied": self.high_confidence_threshold,
                "is_covered": confidence_score >= self.high_confidence_threshold
            },
            "threat_intelligence": {
                "primary_intent": primary_intent,
                "intent_confidence": round(intent_score, 4)
            }
        }

# Global helper for easy integration into the FastAPI services
def selective_prediction(confidence: float, risk_profile: Dict[str, float]):
    manager = RiskManager()
    return manager.evaluate_risk(confidence, risk_profile)