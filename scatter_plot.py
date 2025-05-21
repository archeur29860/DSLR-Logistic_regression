import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from utils import load
from describe import Std


def covariance(X, Y):
    X = list(X)
    Y = list(Y)
    mean_X = sum(X) / len(X)
    mean_Y = sum(Y) / len(Y)
    total = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(len(X)))
    return total / len(X)


def pearson_corr(X, Y):
    cov = covariance(X, Y)
    std_X = Std(X)
    std_Y = Std(Y)
    if std_X == 0 or std_Y == 0:
        return float('nan')
    return cov / (std_X * std_Y)


def best_coef(coefs: dict):
    best = None
    for key, value in coefs.items():
        print(f"{key}: {value}")
        if best is None or abs(value) > abs(best[1]):
            best = (key, value)
    return best


def scatter_plot(data: pd.DataFrame):
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