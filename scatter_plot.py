"""
This script analyzes a dataset to find and visualize the two most correlated features.
It computes Pearson correlation coefficients for all pairs of numerical features
and generates a scatter plot for the most correlated pair.

Usage:
    python scatter_plot.py dataset_train.csv
"""


import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from utils import load
from describe import Std


def covariance(X, Y):
    """
    Compute the covariance between two numerical lists.

    Parameters:
        X (list or array-like): First numerical dataset.
        Y (list or array-like): Second numerical dataset.

    Returns:
        float: The covariance between X and Y.
    """
    X = list(X)
    Y = list(Y)
    mean_X = sum(X) / len(X)
    mean_Y = sum(Y) / len(Y)
    total = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X)))
    return total / len(X)


def pearson_corr(X, Y):
    """
    Compute the Pearson correlation coefficient between two datasets.

    Parameters:
        X (list or array-like): First numerical dataset.
        Y (list or array-like): Second numerical dataset.

    Returns:
        float: The Pearson correlation coefficient between X and Y.
               Returns NaN if one of the standard deviations is zero.
    """
    cov = covariance(X, Y)
    std_X = Std(X)
    std_Y = Std(Y)
    if std_X == 0 or std_Y == 0:
        return float('nan')
    return cov / (std_X * std_Y)


def best_coef(coefs: dict):
    """
    Find the pair of features with the strongest correlation (in absolute value).

    Parameters:
        coefs (dict): Dictionary of feature pair names and their correlation coefficients.

    Returns:
        tuple: A tuple containing the name of the feature pair and the corresponding coefficient.
    """
    best = None
    for key, value in coefs.items():
        print(f"{key}: {value}")
        if best is None or abs(value) > abs(best[1]):
            best = (key, value)
    return best


def scatter_plot(data: pd.DataFrame):
    """
    Compute Pearson correlations between all feature pairs in the dataset,
    identify the most similar pair, and display a scatter plot for that pair.

    Parameters:
        data (pd.DataFrame): The input DataFrame containing the dataset.

    Side effects:
        - Displays and saves a scatter plot of the most correlated feature pair.
        - Prints correlation coefficients and the most similar feature pair.
    """
    try:
        data = data.iloc[:, 6:]
        data = data.dropna()

        coefs = {}
        columns = data.columns

        # Calculate correlations for each pair
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                col1 = columns[i]
                col2 = columns[j]
                coef = pearson_corr(data[col1], data[col2])
                coefs[f"{col1} - {col2}"] = coef

        # Find most similar pair : abs(value) closer to 1
        best_pair = best_coef(coefs)
        print(f"Most similar features: {best_pair[0]} with correlation = {best_pair[1]:.4f}")
        col1, col2 = best_pair[0].split(" - ")
        
        plt.figure(num="Most similar features")
        plt.title("Most similar features")
        
        plt.scatter(data[col1], data[col2])
        plt.xlabel(col1)
        plt.ylabel(col2)

        plt.savefig("img/similar_features.png")
        plt.show()

    except Exception as e:
        print(f"Error: {e}")
    

def main():
    """
    Main function that loads the dataset from command-line arguments
    and generates the scatter plot for the most correlated features.

    Side effects:
        - Loads a CSV file specified via command-line.
        - Calls scatter_plot() on the loaded data.
        - Prints error messages in case of incorrect usage or failure.
    """
    try:
        assert len(sys.argv) == 2, "Usage: python scatter_plot.py dataset_train.csv"

        data = load(sys.argv[1])
        if data is not None:
            scatter_plot(data)
    except AssertionError as e:
        print("AssertionError:", e)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\n bye\n")
        exit(1)