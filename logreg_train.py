import pandas as pd
import matplotlib.pyplot as plt
import sys
from utils import load
# from describe import Std, median, Mean


def gradient_descent()


def main():

    if len(sys.argv) != 2:
        print("Usage: python histogram.py dataset_train.csv")
        return
    data = load(sys.argv[1])



if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
