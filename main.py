from utils import analyze_relationships, interpret_results, save_results
import pandas as pd

def main():
    # Read the data
    df = pd.read_csv('QuestionarioTCC2.csv')

    # Define variables
    independent_vars = ['Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8']
    dependent_vars = ['Q9', 'Q10', 'Q12', 'Q13', 'Q14', 'Q15', 'Q16', 'Q18', 'Q20']

    # Run analysis
    results = analyze_relationships(df, independent_vars, dependent_vars)

    # Save and interpret results
    save_results(results)
    interpret_results(results)

if __name__ == "__main__":
    main()
