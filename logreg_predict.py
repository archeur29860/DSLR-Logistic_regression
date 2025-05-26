from logreg_train import predict_class
import pandas as pd
from utils import load
import sys

def load_normalization_params(filename="normalization_params.txt"):
    with open(filename, "r") as file:
        lines = file.readlines()
        means = []
        stds = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("mean="):
                means = list(map(float, line.strip().split("=")[1].split(",")))
            elif line.startswith("std="):
                stds = list(map(float, line.strip().split("=")[1].split(",")))
        return means, stds


def normalize_w_param(X):
    cols = list(zip(*X))  # transpose
    normalized = []
    means, stds = load_normalization_params()
    for col, mean, std in zip(cols, means, stds):
        normalized.append([(x - mean) / std if std != 0 else 0.0 for x in col])
    return list(map(list, zip(*normalized)))  # re-transpose


def main():
    try:
        assert len(sys.argv) == 2,\
            "Usage: python histogram.py dataset_test.csv"
        data_test = load(sys.argv[1])

        classifiers = {}

        with open("classifiers.txt", "r") as classifiers_file:
            lines = classifiers_file.read().split("\n")
            for line in lines:
                if line == "":
                    break
                class_name, str_values = line.split(":")
                list_values = str_values.split(",")
                list_values[-1], intercept = list_values[-1].split(";")
                classifiers[class_name] = ([float(i) for i in list_values],
                                            float(intercept))

        X_df = data_test.iloc[:, 6:]
        X = X_df.values.tolist()  # list of lists
        X = [[0.0 if pd.isna(xij) else xij for xij in xi] for xi in X]
        
        X = normalize_w_param(X)

        y_pred = [predict_class(xi, classifiers) for xi in X]
        filename = "houses.csv"
        with open(filename, "w") as f:
            f.write("Index,Hogwarts House\n")
            for i in range(len(y_pred)):
                f.write(f"{i},{y_pred[i]}\n")

        labels = data_test.loc[X_df.index, "Hogwarts House"].tolist()
        correct = sum(1 for a, b in zip(labels, y_pred) if a == b)
        accuracy = correct / len(labels)
        print(f"Accuracy sur l'entraînement : {accuracy:.2%}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
