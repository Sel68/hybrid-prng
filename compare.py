import re
import pandas as pd
import matplotlib.pyplot as plt

def parse_nist_result(file_path):
    
    results = []
    current_test = None
    with open(file_path, 'r') as f:
        for line in f:
            # Match test name
            match_test = re.match(r'^\s*([A-Za-z0-9 ]+)$', line.strip())
            if match_test:
                current_test = match_test.group(1).strip()

            # Match p-value and proportion line
            match_result = re.search(r'p-value\s*=\s*([\d\.E+-]+).*proportion\s*=\s*(\d+)/(\d+)', line, re.IGNORECASE)
            if match_result and current_test:
                p_val = float(match_result.group(1))
                passed = int(match_result.group(2))
                total = int(match_result.group(3))
                prop = passed / total
                results.append({'test': current_test, 'p_value': p_val, 'proportion': prop})
                current_test = None  # reset for the next block
    return results


def compare_results(file1, file2, label1='Hybrid PRNG', label2='BBS PRNG'):
    data1 = parse_nist_result(file1)
    data2 = parse_nist_result(file2)

    df1 = pd.DataFrame(data1).set_index('test')
    df2 = pd.DataFrame(data2).set_index('test')

    # Merge on test names
    combined = df1.join(df2, lsuffix=f'_{label1}', rsuffix=f'_{label2}')
    print(combined)

    # Plot p-values
    combined[['p_value_' + label1, 'p_value_' + label2]].plot(kind='bar', figsize=(14, 6), title='P-Value Comparison')
    plt.axhline(0.01, color='red', linestyle='--', label='P-value Threshold (0.01)')
    plt.ylabel("P-Value")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # Plot proportions
    combined[['proportion_' + label1, 'proportion_' + label2]].plot(kind='bar', figsize=(14, 6), title='Proportion of Passed Sequences Comparison')
    plt.axhline(0.96, color='red', linestyle='--', label='Proportion Threshold (~0.96)')
    plt.ylabel("Proportion")
    plt.legend()
    plt.tight_layout()
    plt.show()

compare_results("finalAnalysisReport_Hybrid.txt", "finalAnalysisReport_bbs.txt")
