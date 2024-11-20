from utils import (
    analyze_relationships, 
    interpret_results, 
    save_results,
    validate_sample_size,
    generate_conclusion
)
import pandas as pd
import numpy as np

def main():
    # Read and clean data
    df = pd.read_csv('research.csv')
    df = df.replace('Unknown', np.nan)
    
    # Validate sample size
    validate_sample_size(df)
    
    # Define variables
    independent_vars = ['Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
    dependent_vars = ['Q9', 'Q10', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q18', 'Q20']

    # Run analysis
    results = analyze_relationships(df, independent_vars, dependent_vars)
    
    # Generate and save conclusions
    conclusion = generate_conclusion(results)
    with open('results/statistical_analysis.txt', 'w', encoding='utf-8') as f:
        f.write(conclusion)
    
    # Save detailed results
    save_results(results)
    interpret_results(results)

if __name__ == "__main__":
    main()
