import pandas as pd
import os
from thefuzz import process  # pip install thefuzz[speedup]
from typing import List

def standardize_brands(brands: pd.Series, similarity_threshold: int = 85) -> List[str]:
    """
    Standardize brand names using fuzzy string matching
    
    Args:
        brands: Series of brand names
        similarity_threshold: Minimum similarity score to consider strings as same brand
    
    Returns:
        List of standardized brand names
    """
    # Get unique brand names as reference
    unique_brands = brands.unique().tolist()
    standardized = []
    
    # Create mapping of similar brands
    brand_mapping = {}
    processed_brands = set()
    
    for brand in unique_brands:
        if brand in processed_brands:
            continue
            
        # Find similar brands
        matches = process.extractBests(
            brand, 
            unique_brands, 
            score_cutoff=similarity_threshold
        )
        
        if matches:
            # Use most frequent brand name as the standard
            similar_brands = [m[0] for m in matches]
            counts = brands[brands.isin(similar_brands)].value_counts()
            standard_name = counts.index[0]
            
            # Add all similar brands to mapping
            for match, score in matches:
                brand_mapping[match] = standard_name
                processed_brands.add(match)
    
    # Apply mapping to original series
    return [brand_mapping.get(brand, brand) for brand in brands]

def get_brand_ranking():
    """
    Get ranking of favorite brands from research data
    
    Returns:
        DataFrame: Brands ranked by frequency
    """
    # Read the CSV file
    df = pd.read_csv('research.csv')
    
    # Clean and process Q10 data
    brands = df['Q10'].dropna()
    brands = brands.replace('Unknown', pd.NA).dropna()
    
    # Split multiple brands
    brands = brands.str.split(' - ').explode()
    
    # Clean whitespace and standardize case
    brands = brands.str.strip().str.title()
    
    # Standardize brand names using fuzzy matching
    standardized_brands = standardize_brands(brands)
    
    # Count frequencies
    brand_counts = pd.Series(standardized_brands).value_counts()
    
    # Convert to DataFrame with proper column names
    ranking = pd.DataFrame({
        'Brand': brand_counts.index,
        'Count': brand_counts.values,
        'Percentage': (brand_counts.values / len(standardized_brands) * 100).round(2)
    })
    
    return ranking

def main():
    # Create results directory if it doesn't exist
    os.makedirs('results', exist_ok=True)
    
    # Get and display ranking
    ranking = get_brand_ranking()
    
    print("\nFAVORITE BRANDS RANKING")
    print("=" * 50)
    print(f"Total unique brands: {len(ranking)}")
    print("-" * 50)
    
    # Format and display results
    for idx, row in ranking.iterrows():
        print(f"{idx+1}. {row['Brand']:<20} {row['Count']:>3} mentions ({row['Percentage']}%)")
    
    # Save to CSV
    ranking.to_csv('results/brand_ranking.csv', index=False)
    print(f"\nResults saved to: results/brand_ranking.csv")

if __name__ == "__main__":
    main()
