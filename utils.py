import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings('ignore')
from scipy.stats import chi2_contingency, kruskal
from datetime    import datetime
from scipy import stats
from typing import Dict, List

def cramers_v(x, y):
    """
    Calculate Cramér's V statistic for categorical-categorical association.
    
    Args:
        x: categorical variable
        y: categorical variable
    
    Returns:
        float: Cramér's V statistic
    """
    confusion_matrix = pd.crosstab(x, y)
    chi2, _, _, _ = chi2_contingency(confusion_matrix)
    
    n = confusion_matrix.sum().sum()
    min_dim = min(confusion_matrix.shape) - 1
    
    return np.sqrt(chi2 / (n * min_dim)) if min_dim != 0 else 0

def analyze_relationships(df, independent_cols, dependent_cols):
    """
    Analyze relationships between independent and dependent variables.
    
    Args:
        df: DataFrame containing the data
        independent_cols: List of independent variable column names
        dependent_cols: List of dependent variable column names
    
    Returns:
        Dictionary containing results for each test
    """
    results = {
        'chi_square': [],
        'cramers_v': [],
        'kruskal': []
    }
    
    for dep_col in dependent_cols:
        print(f"\nAnalyzing {dep_col}:")
        
        for ind_col in independent_cols:
            if df[ind_col].nunique() > 1 and df[dep_col].nunique() > 1:
                mask = (df[ind_col] != 'Unknown') & (df[dep_col] != 'Unknown')
                temp_df = df[mask][[ind_col, dep_col]]
                
                if len(temp_df) > 0:
                    contingency_table = pd.crosstab(temp_df[ind_col], temp_df[dep_col])
                    chi2, p_value, _, _ = chi2_contingency(contingency_table)
                    cv = cramers_v(temp_df[ind_col], temp_df[dep_col])
                    
                    results['chi_square'].append({
                        'independent': ind_col,
                        'dependent': dep_col,
                        'chi2': chi2,
                        'p_value': p_value
                    })
                    
                    results['cramers_v'].append({
                        'independent': ind_col,
                        'dependent': dep_col,
                        'coefficient': cv
                    })
                    
                    print(f"\n{ind_col} vs {dep_col}:")
                    print(f"Chi-square p-value: {p_value:.4f}")
                    print(f"Cramér's V: {cv:.4f}")

    return results

def interpret_results(results):
    """
    Interpret the statistical results and provide insights.
    
    Args:
        results: Dictionary containing statistical test results
    """
    significant_relationships = []
    strong_associations = []
    
    for result in results['chi_square']:
        if result['p_value'] < 0.05:
            significant_relationships.append(
                f"{result['independent']} -> {result['dependent']}"
            )
    
    for result in results['cramers_v']:
        if result['coefficient'] > 0.3:
            strong_associations.append(
                f"{result['independent']} -> {result['dependent']} (V={result['coefficient']:.2f})"
            )
    
    print("\nSignificant Relationships (p < 0.05):")
    for rel in significant_relationships:
        print(f"- {rel}")
        
    print("\nStrong Associations (Cramér's V > 0.3):")
    for assoc in strong_associations:
        print(f"- {assoc}")

def save_results(results, base_dir="results"):
    """
    Save analysis results to a text file in the results folder with datetime.
    
    Args:
        results: Dictionary containing statistical test results
        base_dir: Base directory for saving results
    """
    # Create results directory if it doesn't exist
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    # Generate filename with current datetime
    current_time = datetime.now().strftime("%Y%m%d_%H%M")
    filename = os.path.join(base_dir, f"analysis_results_{current_time}.txt")
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("STATISTICAL ANALYSIS RESULTS\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("DETAILED ANALYSIS:\n")
        f.write("-" * 50 + "\n")
        
        for result in results['chi_square']:
            dep = result['dependent']
            ind = result['independent']
            p_value = result['p_value']
            
            cv = next(r['coefficient'] for r in results['cramers_v'] 
                     if r['dependent'] == dep and r['independent'] == ind)
            
            f.write(f"\n{ind} vs {dep}:\n")
            f.write(f"Chi-square p-value: {p_value:.4f}\n")
            f.write(f"Cramér's V: {cv:.4f}\n")
        
        f.write("\n\nSIGNIFICANT RELATIONSHIPS (p < 0.05):\n")
        f.write("-" * 50 + "\n")
        for result in results['chi_square']:
            if result['p_value'] < 0.05:
                f.write(f"- {result['independent']} -> {result['dependent']}\n")
        
        f.write("\n\nSTRONG ASSOCIATIONS (Cramér's V > 0.3):\n")
        f.write("-" * 50 + "\n")
        for result in results['cramers_v']:
            if result['coefficient'] > 0.3:
                f.write(f"- {result['independent']} -> {result['dependent']} ")
                f.write(f"(V={result['coefficient']:.2f})\n")

    print(f"\nResults saved to: {filename}")

def validate_sample_size(df: pd.DataFrame) -> None:
    """
    Validate if sample size meets statistical requirements
    
    Args:
        df: DataFrame with survey data
    """
    total_population = 143500
    sample_size = len(df)
    margin_error = 0.0432
    confidence_level = 0.95
    
    z_score = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    required_size = (z_score**2 * 0.25 * total_population) / (
        (margin_error**2 * (total_population - 1)) + (z_score**2 * 0.25)
    )
    
    print(f"\nSample Size Validation:")
    print(f"Required minimum: {required_size:.0f}")
    print(f"Actual sample: {sample_size}")
    print(f"Margin of Error: {margin_error*100:.2f}%")

def generate_conclusion(results: Dict) -> str:
    """
    Generate comprehensive statistical conclusions
    
    Args:
        results: Dictionary containing statistical test results
    
    Returns:
        str: Formatted conclusion text
    """
    conclusion = "\nSTATISTICAL ANALYSIS RESULTS\n" + "="*50 + "\n\n"
    
    # Count relationship types
    strong_significant = []
    weak_significant = []
    strong_nonsignificant = []
    total_relationships = len(results['chi_square'])
    
    for chi in results['chi_square']:
        vars = (chi['independent'], chi['dependent'])
        cramer = next(c for c in results['cramers_v'] 
                     if c['independent'] == vars[0] and c['dependent'] == vars[1])
        
        if chi['p_value'] < 0.05:
            if cramer['coefficient'] > 0.3:
                strong_significant.append({
                    'vars': vars,
                    'p': chi['p_value'],
                    'v': cramer['coefficient']
                })
            else:
                weak_significant.append({
                    'vars': vars,
                    'p': chi['p_value'],
                    'v': cramer['coefficient']
                })
        elif cramer['coefficient'] > 0.3:
            strong_nonsignificant.append({
                'vars': vars,
                'p': chi['p_value'],
                'v': cramer['coefficient']
            })

    # Summary statistics
    conclusion += f"Total Relationships Analyzed: {total_relationships}\n"
    conclusion += f"Strong & Significant: {len(strong_significant)}\n"
    conclusion += f"Weak but Significant: {len(weak_significant)}\n"
    conclusion += f"Strong but Not Significant: {len(strong_nonsignificant)}\n\n"

    # Detailed findings
    if strong_significant:
        conclusion += "STRONG & SIGNIFICANT RELATIONSHIPS (p < 0.05, V > 0.3):\n"
        conclusion += "-"*50 + "\n"
        for r in strong_significant:
            conclusion += f"• {r['vars'][0]} → {r['vars'][1]}\n"
            conclusion += f"  p={r['p']:.4f}, V={r['v']:.2f}\n"
        conclusion += "\n"
    
    if weak_significant:
        conclusion += "SIGNIFICANT BUT WEAK RELATIONSHIPS (p < 0.05, V ≤ 0.3):\n"
        conclusion += "-"*50 + "\n"
        for r in weak_significant:
            conclusion += f"• {r['vars'][0]} → {r['vars'][1]}\n"
            conclusion += f"  p={r['p']:.4f}, V={r['v']:.2f}\n"
        conclusion += "\n"
    
    if strong_nonsignificant:
        conclusion += "STRONG BUT NOT SIGNIFICANT RELATIONSHIPS (p ≥ 0.05, V > 0.3):\n"
        conclusion += "-"*50 + "\n"
        for r in strong_nonsignificant:
            conclusion += f"• {r['vars'][0]} → {r['vars'][1]}\n"
            conclusion += f"  p={r['p']:.4f}, V={r['v']:.2f}\n"

    return conclusion
