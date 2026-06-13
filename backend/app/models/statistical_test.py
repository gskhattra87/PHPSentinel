import numpy as np
from scipy.stats import chi2

def run_mcnemar_test(y_true, preds_phpsentinel, preds_bigru):
    """
    Computes McNemar's Chi-Squared test for two competing classifiers.
    Focuses entirely on the discordant pairs (where the models disagree).
    """
    # Convert inputs to numpy arrays for vector operations
    y_true = np.array(y_true)
    p_sentinel = np.array(preds_phpsentinel)
    p_bigru = np.array(preds_bigru)
    
    # Track logical correctness vectors
    sentinel_correct = (p_sentinel == y_true)
    bigru_correct = (p_bigru == y_true)
    
    # Count the discordant pairs
    # n10: PHPSentinel is correct, BiGRU is incorrect
    n10 = np.sum(sentinel_correct & ~bigru_correct)
    
    # n01: BiGRU is correct, PHPSentinel is incorrect
    n01 = np.sum(~sentinel_correct & bigru_correct)
    
    print("=== Discordant Disagreement Matrix ===")
    print(f"PHPSentinel Correct / BiGRU Incorrect (n10): {n10}")
    print(f"BiGRU Correct / PHPSentinel Incorrect (n01): {n01}\n")
    
    # Apply McNemar's formula with Edwards' continuity correction
    if (n10 + n01) == 0:
        print("Models have identical disagreement patterns. Cannot compute chi-squared.")
        return
        
    chi2_stat = ((abs(n10 - n01) - 1) ** 2) / (n10 + n01)
    
    # Compute the p-value at 1 degree of freedom
    p_val = chi2.sf(chi2_stat, df=1)
    
    print("=== McNemar's Test Evaluation Results ===")
    print(f"Chi-Squared Statistic (\u03c7\u00b2): {chi2_stat:.2f}")
    print(f"Asymptotic p-value: {p_val:.6f}")
    
    if p_val < 0.01:
        print("Result: Statistically Significant! Reject the null hypothesis (p < 0.01).")
    else:
        print("Result: Not Statistically Significant. Fail to reject the null hypothesis.")

# Mock Execution Example for validation checking
if __name__ == "__main__":
    # Simulate a small test slice matching our thesis performance gap
    # Let's assume out of the test set, there are 153 files where they disagreed
    # PHPSentinel caught 148 of them, while the baseline BiGRU caught only 5
    mock_true = [1] * 153
    mock_sentinel = [1] * 148 + [0] * 5
    mock_bigru = [0] * 148 + [1] * 5
    
    run_mcnemar_test(mock_true, mock_sentinel, mock_bigru)