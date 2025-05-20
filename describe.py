import pandas as pd
import sys
from utils import load


def Mean(args: any):
    '''return the mean of the iterable param'''
    return sum(args) / len(args)


def median(args: int):
    '''return the median of the iterable param'''
    values = list(args)
    values.sort()
    mid = round(len(values)/2)
    return values[mid]


def Q1(args: list):
    '''25% quartile'''
    values = sorted(args)
    return values[int(len(values) * 0.25)]


def Q3(args: list):
    '''75% quartile'''
    values = sorted(args)
    return values[int(len(values) * 0.75)]


def Std(args: int):
    '''return the standard derivation of the iterable param'''
    return var(args) ** 0.5


def var(args: int):
    '''return the variance of the iterable param'''
    meanValue = Mean(args)
    return sum((xi - meanValue)**2 for xi in args) / len(args)


def Min(args: int):
    '''return the minimum int'''
    values = list(args)
    minimum = values[0]
    for val in values:
        if val < minimum:
            minimum = val
    return minimum


def Max(args: int):
    '''return the maximum int'''
    values = list(args)
    maximum = values[0]
    for val in values:
        if val > maximum:
            maximum = val
    return maximum


def Count(args: int):
    '''return the total of line'''
    return len(args)


def apply_functions(data: pd.DataFrame, functions):
    '''Apply a list of functions to all columns and return a
 result DataFrame'''
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
    try:
        assert len(sys.argv) == 2, "Invalid number of parameter"
        data: pd.DataFrame = load(sys.argv[1])
        functions = [Count, Mean, Std, Min, Q1, median, Q3, Max]
        Q1.__name__ = "25%"
        median.__name__ = "50%"
        Q3.__name__ = "75%"

        # delete the 6 first columns
        data = data.iloc[:, 6:]

        # supprimer toutes les lignes avec au moins une cellule vide
        # data = data.dropna(how="any")

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
