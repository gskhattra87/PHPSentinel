import torch
import torch.nn as nn

class TemperatureScaler(nn.Module):
    """
    Implements Temperature Scaling to calibrate the CodeBERT head.
    This aligns model confidence with actual precision.
    """
    def __init__(self):
        super(TemperatureScaler, self).__init__()
        self.temperature = nn.Parameter(torch.ones(1) * 1.5) # Initial T > 1 to soften overconfidence

    def calibrate(self, logits):
        # Scale the logits by temperature before Softmax
        return logits / self.temperature

    def calculate_ece(self, probs, labels, n_bins=10):
        """Calculates Expected Calibration Error as per Guo et al. (2017)."""
        bin_boundaries = torch.linspace(0, 1, n_bins + 1)
        ece = torch.zeros(1)
        
        for bin_lower, bin_upper in zip(bin_boundaries[:-1], bin_boundaries[1:]):
            # Find samples in the current bin
            in_bin = probs.gt(bin_lower.item()) & probs.le(bin_upper.item())
            prop_in_bin = in_bin.float().mean()
            
            if prop_in_bin.item() > 0:
                accuracy_in_bin = labels[in_bin].float().mean()
                avg_confidence_in_bin = probs[in_bin].mean()
                ece += torch.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
        return ece.item()