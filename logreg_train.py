import pandas as pd
import math
import sys
import matplotlib.pyplot as plt
from describe import Max, Min
from utils import load

def save_normalization_params(means, stds, filename="normalization_params.txt"):
    with open(filename, "w") as file:
        means_str = ",".join(map(str, means))
        stds_str = ",".join(map(str, stds))
        file.write(f"mean={means_str}\nstd={stds_str}\n")


def normalize(X):
    """
    Normalize a dataset using standard score normalization (mean = 0, std = 1).

    Args:
        X (list of list of float): Dataset to normalize.

    Returns:
        list of list of float: Normalized dataset.
    """
    cols = list(zip(*X))  # transpose
    normalized = []
    means = []
    stds = []
    for col in cols:
        mean = sum(col) / len(col)
        std = (sum((x - mean) ** 2 for x in col) / len(col)) ** 0.5
        normalized.append([(x - mean) / std for x in col])
        means.append(mean)
        stds.append(std)
    save_normalization_params(means, stds)
    return list(map(list, zip(*normalized)))  # re-transpose


def sigmoid(z):
    """
    Sigmoid activation function.

    Args:
        z (float): Input value.

    Returns:
        float: Output between 0 and 1.
    """
    z = Max([Min([z, 100]), -100])  # clamp to prevent overflow
    return 1 / (1 + math.exp(-z))


def predict_proba(x, w, b):
    """
    Compute the probability prediction using logistic regression.

    Args:
        x (list of float): Input features.
        w (list of float): Weights.
        b (float): Bias.

    Returns:
        float: Probability.
    """
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    return sigmoid(z)


def train_logistic_regression(X, y, epochs=1000, lr=0.1):
    """
    Train a binary logistic regression model using gradient descent.

    Args:
        X (list of list of float): Input features.
        y (list of int): Binary labels.
        epochs (int): Number of iterations.
        lr (float): Learning rate.

    Returns:
        tuple: weights (list), bias (float)
    """
    w = [0.0] * len(X[0])
    b = 0.0

    for epoch in range(epochs):
        for xi, yi in zip(X, y):
            pred = predict_proba(xi, w, b)
            error = pred - yi
            for j in range(len(w)):
                w[j] -= lr * error * xi[j]
            b -= lr * error
    return w, b


def predict_class(x, classifiers):
    """
    Predict the class using one-vs-all classifiers.

    Args:
        x (list of float): Input features.
        classifiers (dict): Dictionary of (weights, bias) per class.

    Returns:
        str: Predicted class.
    """
    probs = {}
    for c in classifiers:
        w, b = classifiers[c]
        probs[c] = predict_proba(x, w, b)
    
    # find and return the house with the highest probability
    max_value = Max(list(probs.values()))

    for c, p in probs.items():
        if p == max_value:
            return c


def save_classifiers(classifiers, filename="classifiers.txt"):
    """
    Save trained classifiers to a text file.

    Args:
        classifiers (dict): Dictionary of class to (weights, bias).
        filename (str): Output file name.
    """
    with open(filename, "w") as f:
        for class_name, (weights, bias) in classifiers.items():
            weights_str = ",".join(f"{w}" for w in weights)
            f.write(f"{class_name}:{weights_str};{bias}\n")


def main():
    """
    Main training function: loads data, trains model, evaluates, and saves results.
    """
    assert len(sys.argv) == 2, "Invalid number of arguments.\nUsage: python logreg_train.py <data.csv>"
    data = load(sys.argv[1])

    # Select only numeric features
    X_df = data.iloc[:, 6:]
    X = X_df.values.tolist()

    # Get target labels
    labels = data.loc[X_df.index, "Hogwarts House"].tolist()
    classes = sorted(set(labels))
    X = [[0.0 if pd.isna(xij) else xij for xij in xi] for xi in X]

    X = normalize(X)

    # Train one-vs-all classifiers
    classifiers = {}
    for c in classes:
        y_c = [1 if label == c else 0 for label in labels]
        w, b = train_logistic_regression(X, y_c, epochs=1000, lr=0.1)
        classifiers[c] = (w, b)

    # Make predictions on the training set
    y_pred = [predict_class(xi, classifiers) for xi in X]

    # Compute accuracy
    correct = sum(1 for a, b in zip(labels, y_pred) if a == b)
    accuracy = correct / len(labels)
    print(f"Training accuracy: {accuracy:.2%}")

    # Save classifiers
    save_classifiers(classifiers)

    # Prepare prediction breakdown
    counts = {c: [0, 0] for c in classes}
    for true, pred in zip(labels, y_pred):
        if true == pred:
            counts[true][0] += 1
        else:
            counts[pred][1] += 1

    # Visualization
    labels_x = list(counts.keys())
    corrects = [v[0] for v in counts.values()]
    errors = [v[1] for v in counts.values()]

    bar_width = 0.35
    x = range(len(labels_x))

    plt.bar(x, corrects, width=bar_width, label="Correct", color='green')
    plt.bar([i + bar_width for i in x], errors, width=bar_width, label="Incorrect", color='red')
    plt.xticks([i + bar_width / 2 for i in x], labels_x)
    plt.title("Prediction Breakdown by Class")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
