'''
#Original formula
import pandas as pd

def get_highly_correlated_features(data, threshold):
    corrmatrix = data.corr(numeric_only=True)
    correlated_features = {}
    for i in range(len(corrmatrix.columns)):
        for j in range(i+1, len(corrmatrix.columns)):
            if abs(corrmatrix.iloc[i, j]) > threshold:
                colname_i = corrmatrix.columns[i]
                colname_j = corrmatrix.columns[j]
                correlation_coefficient = corrmatrix.iloc[i, j]
                pair = (colname_i, colname_j)
                correlated_features[pair] = correlation_coefficient
    return correlated_features

'''

import pandas as pd
from RegressionPackage.plot_module import plot_correlation_scatter

"""
    Extracts highly correlated features from a given dataset based on a specified threshold.

    Args:
        data (pandas.DataFrame): The input dataset.
        threshold (float): The correlation threshold above which features are considered highly correlated.

    Returns:
        dict: A dictionary containing pairs of correlated features and their corresponding correlation coefficients.

    Note:
        - The user is prompted to enter column names to exclude from the analysis. If no columns are specified, all columns are included.
        - The function checks if the entered columns exist in the dataset and prompts the user to enter valid columns if any are invalid.
        - The function excludes non-numeric columns from the selected data.
        - The function calculates the correlation matrix of the selected data and identifies pairs of highly correlated features.
        - The function prints the results of the highly correlated features and prompts the user to visualize the data if desired.
        - The function returns a dictionary containing pairs of correlated features and their correlation coefficients.

"""


def get_highly_correlated_features(data, threshold):
    print("Welcome to the Highly Correlated Features Extractor!")
    while True:
        # Get user input for column names to exclude
        exclude_columns_str = input("Enter the column names to exclude (comma-separated), or press Enter for none: ")
        if exclude_columns_str.strip() == "":
            # If no columns to exclude, proceed with all columns
            selected_data = data
            break
        
        exclude_columns = exclude_columns_str.split(',')
        
        # Check if all entered columns exist in the DataFrame
        invalid_columns = [col for col in exclude_columns if col not in data.columns]
        if invalid_columns:
            print("The following column(s) do not exist in the DataFrame: {}".format(", ".join(invalid_columns)))
            print("Please try again.")
        else:
            # Exclude specified columns
            selected_data = data.drop(columns=exclude_columns)
            
            break  # All entered columns are valid, exit loop
    
    # Exclude non-numeric columns
    numeric_columns = selected_data.select_dtypes(include=['number']).columns
    selected_data = selected_data[numeric_columns]

    corrmatrix = selected_data.corr()
    correlated_features = {}
    for i in range(len(corrmatrix.columns)):
        for j in range(i+1, len(corrmatrix.columns)):
            if abs(corrmatrix.iloc[i, j]) > threshold:
                colname_i = corrmatrix.columns[i]
                colname_j = corrmatrix.columns[j]
                correlation_coefficient = corrmatrix.iloc[i, j]
                pair = (colname_i, colname_j)
                correlated_features[pair] = correlation_coefficient
    
    print('Correlated Feature Results:', correlated_features)
    # Ask user if they want to visualize the data
    visualize = input("Would you like to visualize the data(Scatter Plot) (yes/no)? ").lower()
    if visualize == "yes":
        plot_correlation_scatter(correlated_features, data)
    
    return correlated_features

# Your additional code or function calls can be added here






