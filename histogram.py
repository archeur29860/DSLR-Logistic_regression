import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


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


def plot_histograms(data):
    '''Show all histograms on a single page using subplots'''
    houses = data["Hogwarts House"].unique()
    features = [col for col in data.columns if col not in ["Index", "Hogwarts House", "First Name", "Last Name", "Birthday", "Best Hand"]]
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
            ax.hist(house_data, alpha=0.6, bins=20, label=house, color=house_colors.get(house, 'pink'))

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
    if data is not None:
        plot_histograms(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\n bye\n")
        exit(1)
