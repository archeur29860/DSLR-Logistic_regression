from logreg_train import predict_class, normalize
import pandas as pd
from utils import load


def main():
    try:
    data_test = load("datasets/dataset_test.csv")

    classifiers = {}

    with open("classifiers.txt", "r") as classifiers_file:
        lines = classifiers_file.read().split("\n")
        for line in lines:
            if line == "":
                break
            class_name, str_values = line.split(":")
            list_values = str_values.split(",")
            list_values[-1], intercept = list_values[-1].split(";")
            classifiers[class_name] = ([float(i) for i in list_values], float(intercept))

    X_df = data_test.iloc[:, 6:]
    X = X_df.values.tolist()  # list of lists
    X = [[0.0 if pd.isna(xij) else xij for xij in xi] for xi in X]


    X = normalize(X)

    y_pred = [predict_class(xi, classifiers) for xi in X]
    filename = "houses.csv"
    with open(filename, "w") as f:
        f.write("Index,Hogwarts House\n")
        for i in range(len(y_pred)):
            f.write(f"{i},{y_pred[i]}\n")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
