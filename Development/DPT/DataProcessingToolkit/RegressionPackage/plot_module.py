import matplotlib.pyplot as plt

def plot_correlation_scatter(correlated_features, data):
    """
    Plot scatter plots for highly correlated feature pairs.

    Parameters:
        correlated_features (dict): A dictionary containing pairs of highly correlated features
                                    along with their correlation coefficient.
        data (DataFrame): The DataFrame containing the dataset.
    """
    for pair, correlation_coefficient in correlated_features.items():
        feature1, feature2 = pair
        plt.figure(figsize=(8, 6))
        plt.scatter(data[feature1], data[feature2], alpha=0.7)
        plt.title(f'Scatter plot of {feature1} vs {feature2}')
        plt.xlabel(feature1)
        plt.ylabel(feature2)
        plt.grid(True)
        plt.text(0.1, 0.9, f'Correlation coefficient: {correlation_coefficient:.2f}',
                 transform=plt.gca().transAxes)
        plt.show()



