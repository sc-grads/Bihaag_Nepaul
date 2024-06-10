import pandas as pd
from RegressionPackage.correlation_module import get_highly_correlated_features
from RegressionPackage.plot_module import plot_correlation_scatter
from CleaningPackage.removingdups_module import remove_highly_correlated_features
from CleaningPackage.cleaning_module import handle_missing_valuestwo
from ExportPackage.export_module import create_table_and_insert_data




#1 Handle Missing Values

data = pd.read_csv('Mall_Customers.csv')
data_handled = handle_missing_valuestwo(data, method='zero')


# Print the first few rows of the handled data
print(data_handled)




#2 Get Highly Correlated Features or Plot Data Correlations

corr_features = get_highly_correlated_features(data_handled, 0.80)
print(corr_features)



#3 Plot Results
'''
data = pd.read_csv('muffins_cupcakes.csv')
# Get highly correlated features
correlated_features = {('Flour', 'Sugar'): -0.8234974146842132}

# Plot scatter plots for highly correlated features
plot_correlation_scatter(correlated_features, data)
'''


#3 Remove Highly Correlated Features or Remove Duplicates from Dataset
'''
# Example usage
data = remove_highly_correlated_features(data, correlated_features)

print(data)
'''




#5 Export Data to sql table

# Call the function with the DataFrame and desired table name
create_table_and_insert_data(data_handled, 'Mall_Customers')
