import pandas as pd
import os
import sys

def load(path: str, index_column=None) -> pd.DataFrame:
    '''Load a csv file into DataFrame from pandas with a column index ->
 default set to None'''
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(script_dir, path)

        data = pd.read_csv(csv_path, index_col=index_column)
        return data
    except Exception:
        print(f"Error: no such a file or directory: {path}")
    return None

def mean(args: any):
    '''return the mean of the iterable param'''
    return sum(args) / len(args)


def median(args: int):
    '''return the median of the iterable param'''
    values = list(args)
    values.sort()
    mid = round(len(values)/2)
    return values[mid]


def quartile(args: int):
    '''return the first and third quratiles of the iterable param'''
    values = list(args)
    values.sort()
    first = round(len(values)/4)
    third = first * 3
    return values[first], values[third]


def std(args: int):
    '''return the standard derivation of the iterable param'''
    return var(args) ** 0.5


def var(args: int):
    '''return the variance of the iterable param'''
    meanValue = mean(args)
    return sum((xi - meanValue)**2 for xi in args) / len(args)


def main():
    try:
        assert len(sys.argv) == 2, "Invalid number of parameter"
        data = load(sys.argv[1])
        data.describe()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
