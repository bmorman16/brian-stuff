import pandas as pd
from scipy.stats import pearsonr

# Load independent variables
df_independent = pd.read_csv('EMBA60_TeamB_Consulting_Independent.csv')

# Load dependent variables
df_dependent = pd.read_csv('EMBA60_TeamB_Consulting_Dependent.csv')

# Check the shape and first few rows to confirm loading
print(df_independent.shape)
print(df_independent.head())

print(df_dependent.shape)
print(df_dependent.head())
correlation_results = pd.DataFrame(index=df_independent.columns, columns=df_dependent.columns)
pvalue_results = pd.DataFrame(index=df_independent.columns, columns=df_dependent.columns)

for ind_var in df_independent.columns:
    for dep_var in df_dependent.columns:
        corr, pval = pearsonr(df_independent[ind_var], df_dependent[dep_var])
        correlation_results.loc[ind_var, dep_var] = corr
        pvalue_results.loc[ind_var, dep_var] = pval

print("Correlation coefficients:")
print(correlation_results)

print("\nP-values:")
print(pvalue_results)

correlation_results.to_csv('correlation_results.csv')
pvalue_results.to_csv('pvalue_results.csv')

print("Correlation results saved to 'correlation_results.csv'")
print("P-value results saved to 'pvalue_results.csv'")
