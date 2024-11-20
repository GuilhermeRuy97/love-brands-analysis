# Love Brands Analysis: Consumer Brand Perception Study
Research analyzing how consumers in Poços de Caldas (MG, Brazil) perceive and connect with their preferred brands. This academic study examines correlations between demographic variables and brand relationships through statistical analysis.

# Steps to run the project
1. Create a virtual environment: `python -m venv venv`
    - activate: `.\venv\Scripts\activate`
2. Install the dependencies from `pip install -r requirements.txt`
3. Run the project: `python main.py`
4. See the results in the `results` folder

# Data Dictionary
- Q1: Email address
- Q2: Do you live in or near any of these neighborhoods?
- Q3: What gender do you identify with?
- Q4: What is your marital status?
- Q5: What is your age range?
- Q6: What is your education?
- Q7: Which of the options below do you consume the most?
- Q8: Within the option previously chosen - do you generally prefer local - national or global brands?
- Q9: In your opinion - what is most important to you in a brand?
- Q10: What is your favorite brand? (Name just one)
- Q11: Which area is this brand part of?
- Q12: What is most important to you about your favorite brand?
- Q13: What is the brand's style?
- Q14: What is your relationship with this brand?
- Q15: How connected do you feel to this brand?
- Q16: Where do you follow the latest news from this brand?
- Q17: Do you remember any advertising campaigns for this brand?
- Q18: Have you ever purchased a product from this brand due to the influence of a specific campaign?
- Q19: Where do you see this brand appearing the most?
- Q20: What attracts you most about the brand you chose?

# Data Source:
- The population estimated by IBGE for Poços de Caldas in 2024 is 171533.
- Children must be disregarded from the total population so as not to have a population bias that cannot consume on their own. Therefore, the estimate of 16.33% of the total population (under 14 years old) is disregarded.
- The considered population of Poços de Caldas is 143,500.
The sample space of the population of Poços de Caldas is 500 (500 people were surveyed).

- Given the following margin of error formula for proportions in finite populations:
![margin of error formula](./assets/margin-of-error-formula.png)
- We have that the margin of error is approximately: 4.32%

# Output (result files)
This will create a statistical_analysis.txt file that categorizes relationships into three groups:
1. Strong and Significant: p < 0.05 AND V > 0.3
- Most reliable relationships
- Both statistically significant and strong association
2. Significant but Weak: p < 0.05 BUT V ≤ 0.3
- Real relationship exists
- But the association is weak
3. Strong but Not Significant: p ≥ 0.05 BUT V > 0.3
- Strong association appears
- But could be due to chance/small sample size