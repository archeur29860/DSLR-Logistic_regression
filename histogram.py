import pandas as pd
import matplotlib.pyplot as plt
import sys
from utils import load
from describe import Std


def find_homogenous_course(data: pd.DataFrame, col_course, col_house="Hogwarts House"):
    '''Find the most homogenous course'''
    G = []
    H = []
    R = []
    S = []
    # print(data)
    for i in data["Index"]:
        house = data[col_house][i]
        # print(house)
        # print(data[col_course][i], col_course)
        match house:
            case "Gryffindor":
                G.append(data[col_course][i])
            case "Hufflepuff":
                H.append(data[col_course][i])
            case "Ravenclaw":
                R.append(data[col_course][i])
            case "Slytherin":
                S.append(data[col_course][i])
            case _:
                print("No house")
    # print(G)
    # print(G)
    # print(G)
    # print(S)
    res = (Std(G) + Std(H) + Std(R) + Std(S)) / 4
    return res




def plot_histograms(data: pd.DataFrame):
    '''Show all histograms on a single page using subplots'''
    houses = data["Hogwarts House"].unique()
    features = [
        col for col in data.columns if col not in [
            "Index", "Hogwarts House", "First Name", "Last Name", "Birthday",
            "Best Hand"]]
    house_colors = {
        "Gryffindor": "#740001",
        "Hufflepuff": "#EEBA35",
        "Ravenclaw": "#0F1D4A",
        "Slytherin": "#1A472A"
    }

    num_features = len(features)
    cols = 3
    rows = (num_features + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    axes = axes.flatten()

    for i, feature in enumerate(features):
        ax = axes[i]
        for house in houses:
            house_data = data[data["Hogwarts House"] == house][feature].dropna()
            ax.hist(
                house_data,
                alpha=0.6,
                bins=20,
                label=house,
                color=house_colors.get(house, 'pink'))

        ax.set_title(feature)
        ax.set_xlabel("Score")
        ax.set_ylabel("Count")
        ax.grid(True)
        ax.legend()

    # remove the grid if features < rows * cols
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()


def main():

    if len(sys.argv) != 2:
        print("Usage: python histogram.py dataset_train.csv")
        return
    data = load(sys.argv[1])
    res = []
    if data is not None:
        for col in data.iloc[:, 6:].columns:
            res.append(find_homogenous_course(data.dropna(subset=[col]), col))
            print(f"{col}: {res[-1]}")
        plot_histograms(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
