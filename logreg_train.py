import pandas as pd
import math
import matplotlib.pyplot as plt

def normalize(X):
    cols = list(zip(*X))  # transpose
    normalized = []
    for col in cols:
        mean = sum(col) / len(col)
        std = (sum((x - mean) ** 2 for x in col) / len(col)) ** 0.5
        normalized.append([(x - mean) / std for x in col])
    return list(map(list, zip(*normalized)))  # retranspose


# Sigmoid : fonction d'activation logistique
def sigmoid(z):
    # Limiter z pour éviter les overflow
    z = max(min(z, 100), -100)
    return 1 / (1 + math.exp(-z))

# Hypothèse (probabilité pour une classe)
def predict_proba(x, w, b):
    z = sum(xi * wi for xi, wi in zip(x, w)) + b
    return sigmoid(z)

# Entraînement d'un classifieur binaire avec descente de gradient
def train_logistic_regression(X, y, epochs=1000, lr=0.1):
    w = [0.0] * len(X[0])  # initialisation des poids
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
    # On choisit la classe dont le modèle donne la probabilité la plus haute
    probs = {}
    for c in classifiers:
        w, b = classifiers[c]
        probs[c] = predict_proba(x, w, b)
    return max(probs, key=probs.get)


def save_classifiers(classifiers, filename="classifiers.txt"):
    with open(filename, "w") as f:
        for class_name, (weights, bias) in classifiers.items():
            weights_str = ",".join(f"{w}" for w in weights)
            f.write(f"{class_name}:{weights_str};{bias}\n")


def main():
    # Lire le CSV
    data = pd.read_csv("datasets/dataset_train.csv")

    # Garder uniquement les colonnes numériques (features)
    X_df = data.select_dtypes(include=["float64", "int64"]).dropna()
    X = X_df.values.tolist()  # liste de listes

    # Récupérer les classes cibles (maisons)
    labels = data.loc[X_df.index, "Hogwarts House"].tolist()
    classes = sorted(set(labels))  # ex: ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']

    X = normalize(X)

    # Dictionnaire pour stocker les modèles par classe
    classifiers = {}

    for c in classes:
        # y_c est 1 si la classe est c, 0 sinon
        y_c = [1 if label == c else 0 for label in labels]
        w, b = train_logistic_regression(X, y_c, epochs=1000, lr=0.1)
        classifiers[c] = (w, b)

    # Prédire sur l'ensemble d'entraînement
    y_pred = [predict_class(xi, classifiers) for xi in X]


    correct = sum(1 for a, b in zip(labels, y_pred) if a == b)
    accuracy = correct / len(labels)
    print(f"Accuracy sur l'entraînement : {accuracy:.2%}")


    # Afficher la distribution des vraies vs. prédictions
    counts = {c: [0, 0] for c in classes}
    for true, pred in zip(labels, y_pred):
        if true == pred:
            counts[true][0] += 1
        else:
            counts[pred][1] += 1

    save_classifiers(classifiers)

    # Affichage
    labels_x = list(counts.keys())
    corrects = [v[0] for v in counts.values()]
    errors = [v[1] for v in counts.values()]

    bar_width = 0.35
    x = range(len(labels_x))

    plt.bar(x, corrects, width=bar_width, label="Correct", color='green')
    plt.bar([i + bar_width for i in x], errors, width=bar_width, label="Incorrect", color='red')
    plt.xticks([i + bar_width / 2 for i in x], labels_x)
    plt.title("Répartition des prédictions")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
