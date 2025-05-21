"""
This script computes descriptive statistics (count, mean, std deviation, quartiles, etc.)
for numerical columns in a dataset. Usage: python describe.py dataset_train.csv
"""

import pandas as pd
import sys
from utils import load


def Mean(args: any):
    """
    Calculate the mean of a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The arithmetic mean.
    """
    return sum(args) / len(args)


def median(args: int):
    """
    Calculate the median of a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The median value.
    """
    values = list(args)
    values.sort()
    mid = round(len(values)/2)
    return values[mid]


def Q1(args: list):
    """
    Compute the 25th percentile (first quartile) of the data.

    Parameters:
        args (list): A list of numeric values.

    Returns:
        float: The Q1 value.
    """
    values = sorted(args)
    return values[int(len(values) * 0.25)]


def Q3(args: list):
    """
    Compute the 75th percentile (third quartile) of the data.

    Parameters:
        args (list): A list of numeric values.

    Returns:
        float: The Q3 value.
    """
    values = sorted(args)
    return values[int(len(values) * 0.75)]


def Std(args: int):
    """
    Calculate the standard deviation of a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The standard deviation.
    """
    return var(args) ** 0.5


def var(args: int):
    """
    Calculate the variance of a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The variance.
    """
    meanValue = Mean(args)
    return sum((xi - meanValue)**2 for xi in args) / len(args)


def Min(args: int):
    """
    Return the minimum value in a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The minimum value.
    """
    values = list(args)
    minimum = values[0]
    for val in values:
        if val < minimum:
            minimum = val
    return minimum


def Max(args: int):
    """
    Return the maximum value in a numeric iterable.

    Parameters:
        args (iterable): A list or array of numeric values.

    Returns:
        float: The maximum value.
    """
    values = list(args)
    maximum = values[0]
    for val in values:
        if val > maximum:
            maximum = val
    return maximum


def Count(args: int):
    """
    Count the number of elements in an iterable.

    Parameters:
        args (iterable): A list or array of values.

    Returns:
        int: The number of elements.
    """
    return len(args)


def apply_functions(data: pd.DataFrame, functions):
    """
    Apply a list of statistical functions to each column of a DataFrame.

    Parameters:
        data (pd.DataFrame): The input DataFrame.
        functions (list): A list of functions to apply.

    Returns:
        pd.DataFrame: A DataFrame with function names as rows and column names as columns.
    """
    results = {}
    for col in data.columns:
        data = data.dropna(subset=[col])
        stats = {}
        for func in functions:
            try:
                stats[func.__name__] = func(data[col].dropna())
            except Exception:
                stats[func.__name__] = 'NaN'
        results[col] = stats
    return pd.DataFrame(results)


def main():
    """
    Main function that loads the dataset, removes non-numerical columns,
    applies descriptive statistics functions, and prints the result.
    """
    try:
        assert len(sys.argv) == 2, "Invalid number of parameter"
        data: pd.DataFrame = load(sys.argv[1])
        functions = [Count, Mean, Std, Min, Q1, median, Q3, Max]
        Q1.__name__ = "25%"
        median.__name__ = "50%"
        Q3.__name__ = "75%"

        # delete the 6 first columns
        data = data.iloc[:, 6:]

        # apply functions and print DataFrame
        result_df = apply_functions(data, functions)
        print(result_df)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
