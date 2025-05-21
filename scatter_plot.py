import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from describe import Std


house_colors = {
    "Gryffindor": "#740001",
    "Hufflepuff": "#EEBA35",
    "Ravenclaw": "#0F1D4A", 
    "Slytherin": "#1A472A" 
}


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


def covariance(X, Y):
    n = len(X)
    if n != len(Y):
        raise ValueError("Both list must be the same lenght.")

    mean_X = sum(X) / n
    mean_Y = sum(Y) / n

    total = 0
    for i in range(n):
        total += (X[i] - mean_X) * (Y[i] - mean_Y)

    return total / (n - 1)


def pearson_corr(X, Y):
    cov = covariance(X, Y)
    std_X = Std(X)
    std_Y = Std(Y)
    return cov / (std_X * std_Y)



#+1 → quand X augmente, Y augmente parfaitement (ex : taille et poids dans une population homogène)

#–1 → quand X augmente, Y diminue parfaitement (ex : vitesse ↔️ temps pour un même trajet)

#0 → aucune tendance linéaire (ex : taille d’une personne et son numéro de téléphone)

def scatter_plot(data: pd.DataFrame):
    try:


    except Exception as e:
        print(f"Error: {e}")
    

def main():
    if len(sys.argv) != 2:
        print("Usage: python scatter_plot.py dataset_train.csv")
        return
    data = load(sys.argv[1])
    if data is not None:
        scatter_plot(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\n bye\n")
        exit(1)