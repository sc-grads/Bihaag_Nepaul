def remove_highly_correlated_features(data, correlated_features):
    """
    Remove highly correlated features from the dataset.

    Parameters:
        data (DataFrame): The input DataFrame containing the dataset.
        correlated_features (dict): A dictionary containing pairs of highly correlated features
                                    along with their correlation coefficient.

    Returns:
        DataFrame: The DataFrame with highly correlated features removed.
    """
    # Get the names of columns to drop
    columns_to_drop = [pair[1] for pair in correlated_features.keys()]

    # Drop the highly correlated features from the dataset
    data = data.drop(columns=columns_to_drop)

    return data