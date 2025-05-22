import math
import pandas as pd
import matplotlib.pyplot as plt
import sys
from utils import load
# from describe import Std, median, Mean


import matplotlib.pyplot as plt
import pandas as pd
from utils import load


house_colors = {
    "Gryffindor": "#740001",
    "Hufflepuff": "#EEBA35",
    "Ravenclaw" : "#0F1D4A",
    "Slytherin" : "#1A472A"
}


def extract_and_clean_columns(data, columns, class_column_name="Hogwarts House"):
    new_data = data[[class_column_name] + columns]
    new_data = new_data.dropna()
    return new_data


def extract_one_house_vs_all(selected_house, data):

    one = data[selected_house]
    all_house = []

    for i in data.keys():
        if i != selected_house:
            all_house += data[i]

    return one, all_house


def separate_class(data, x_column, y_column, class_column_name="Hogwarts House"):
    sep_data = {}
    houses = data[class_column_name].unique()
    for house in houses:
            x_data = data[data[class_column_name] == house][x_column]
            y_data = data[data[class_column_name] == house][y_column]
            sep_data[house] = ([(x_data.iloc[i], y_data.iloc[i]) for i in range(len(x_data))])
    return sep_data


def logistic_regression(one, all, learning_rate=0.01, iteration=1000):
    return 0
    
    


def main():

    if len(sys.argv) != 2:
        print("Usage: python histogram.py dataset_train.csv")
        return
    
    data = load(sys.argv[1])
    columns = data.iloc[:, 6:].columns
    houses = data["Hogwarts House"].unique()
    
    ## Afficher l'ensemble des graphs pour chaque maison croisée avec les features

    # Construction des couples de colonnes
    column_pairs = []
    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            column_pairs.append((columns[i], columns[j]))
    
    n_plots = len(column_pairs)
    n_cols = 8 # plus de colonnes pour une grille plus compacte
    n_rows = math.ceil(n_plots / n_cols)
    
    for selected_house in houses:
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(2 * n_cols, 2 * n_rows))  # figure compacte
        fig.suptitle(f"{selected_house} - pairplot style", fontsize=12)
        axes = axes.flatten()
    
        for idx, (col_x, col_y) in enumerate(column_pairs):
            tmp_data = extract_and_clean_columns(data, [col_x, col_y])
            sep_data = separate_class(tmp_data, col_x, col_y)
            one, all_house = extract_one_house_vs_all(selected_house, sep_data)
    
            ax = axes[idx]
            ax.scatter([x for x, y in all_house], [y for x, y in all_house], color="gray", alpha=0.2, s=5)
            ax.scatter([x for x, y in one], [y for x, y in one], color=house_colors[selected_house], alpha=0.6, s=5)
            ax.set_title(f"{col_x[:5]} vs {col_y[:5]}", fontsize=6)
            ax.tick_params(labelsize=5)
            ax.set_xticks([])
            ax.set_yticks([])
            ax.grid(False)
    
        # Supprimer les axes vides
        for j in range(idx + 1, len(axes)):
            fig.delaxes(axes[j])
    
        plt.tight_layout(rect=[0, 0.03, 1, 0.95], h_pad=0.5, w_pad=0.5)
        plt.show()

# Boucle pour print les graphs un à un
# for selected_house in houses:
    # for i in range(len(columns)):
        # for j in range(i + 1, len(columns)):
            # tmp_data = extract_and_clean_columns(data, [columns[i], columns[j]])
            # sep_data = separate_class(tmp_data, columns[i], columns[j])
            # one, all_house = extract_one_house_vs_all(selected_house, sep_data)
            # plt.scatter([ x for x, y in all_house], [ y for x, y in all_house], color="blue")
            # plt.scatter([ x for x, y in one], [ y for x, y in one], color="pink")
    # 
            # plt.show()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
