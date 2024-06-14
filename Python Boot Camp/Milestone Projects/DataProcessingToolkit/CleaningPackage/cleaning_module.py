import pandas as pd

def handle_missing_values(data, method='mean'):
    """
    Handle missing values in a DataFrame.

    Parameters:
        data (DataFrame): The input DataFrame with missing values.
        method (str): The method to handle missing values. Options are:
            - 'mean': Replace missing values with the mean of the column.
            - 'median': Replace missing values with the median of the column.
            - 'mode': Replace missing values with the mode of the column.
            - 'ffill': Forward fill missing values using the last valid observation.
            - 'bfill': Backward fill missing values using the next valid observation.
            - 'drop': Drop rows with missing values.

    Returns:
        DataFrame: The DataFrame with missing values handled.
    """

    '''
    if method == 'mean':
        return data.fillna(data.mean())
    elif method == 'median':
        return data.fillna(data.median())
    elif method == 'mode':
        return data.fillna(data.mode().iloc[0])
    elif method == 'ffill':
        return data.ffill()
    elif method == 'bfill':
        return data.bfill()
    elif method == 'drop':
        return data.dropna()
    else:
        raise ValueError("Invalid method. Supported methods are 'mean', 'median', 'mode', 'ffill', 'bfill', or 'drop'.")

'''


def handle_missing_valuestwo(data, method='mean'):
    print("Welcome to the Missing Value Handler! The data you passed will be processed.")
    # Exclude non-numeric columns
    numeric_data = data.select_dtypes(include=['number'])

    if method == 'mean':
        return numeric_data.fillna(numeric_data.mean())
    elif method == 'median':
        return numeric_data.fillna(numeric_data.median())
    elif method == 'mode':
        return numeric_data.fillna(numeric_data.mode().iloc[0])
    elif method == 'ffill':
        return numeric_data.ffill()
    elif method == 'bfill':
        return numeric_data.bfill()
    elif method == 'drop':
        return numeric_data.dropna()
    elif method == 'zero':
        return data.fillna(0)
    else:
        raise ValueError("Invalid method. Supported methods are 'mean', 'median', 'mode', 'ffill', 'bfill', or 'drop'.")
