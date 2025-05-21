import pandas as pd
import matplotlib.pyplot as plt
import sys
from utils import load
from describe import Std, median, Mean


house_colors = {
    "Gryffindor": "#740001",
    "Hufflepuff": "#EEBA35",
    "Ravenclaw": "#0F1D4A",
    "Slytherin": "#1A472A"
}


def ft_levene(groups):
    '''Levene test'''
    k = len(groups)
    n_total = sum(len(note) for note in groups)

    # 1 - median
    median_house = [median(note) for note in groups]
    # print(f"median : {median_house}")

    # 2 - absolute deviations from median,
    Z_ij_all = []
    for group in groups:
        med = median(group)
        Z_ij_all.append([abs(i - med) for i in group])

    # 3 - calculate mean of all Z,
    mean_Zij = []
    for i in range(k):
        mean_Zij.append(Mean(Z_ij_all[i]))

    # 4 - calculate mean of Z,
    mean_Zij_total = Mean(mean_Zij)

    # 5 - calculate of the numerator of the statistic
    numerator = 0
    for i in range(k):
        numerator += len(Z_ij_all[i]) * ((mean_Zij[i] - mean_Zij_total) ** 2)

    # 6 - Denominator 
    dem = 0
    for i in range(k):
        dem_group = []
        for Z_ij in Z_ij_all[i]:
            # print(f"Zij: {Z_ij}")
            dem_group.append((Z_ij - mean_Zij[i]) ** 2)
            # print(dem_group)
        dem += sum(dem_group)
        # print(dem)

    # statistic calculation of W
    W = ((n_total - k) / (k - 1)) * (numerator / dem)

    return(W)

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
    res = ft_levene([G, H, R, S])
    return res


def plot_histograms(data: pd.DataFrame):
    '''Show all histograms on a single page using subplots'''
    houses = data["Hogwarts House"].unique()
    features = [
        col for col in data.columns if col not in [
            "Index", "Hogwarts House", "First Name", "Last Name", "Birthday",
            "Best Hand"]]

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
    plt.savefig("img/histo_all_course.png")
    plt.show()


def plot_histograms_homogenous(course, data):
    houses = data["Hogwarts House"].unique()
    fig, ax = plt.subplots(figsize=(8, 6))
    for house in houses:
        house_data = data[data["Hogwarts House"] == house][course].dropna()
        ax.hist(
            house_data,
            alpha=0.6,
            bins=20,
            label=house,
            color=house_colors.get(house, 'pink'))

    ax.set_title("the most homogenous course : " + course)
    ax.set_xlabel("Score")
    ax.set_ylabel("Count")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.savefig("img/homogenous_course.png")
    plt.show()


def main():
    try:
        if len(sys.argv) != 2:
            print("Usage: python histogram.py dataset_train.csv")
            return
        data = load(sys.argv[1])
        res = {}
        if data is not None:
            for col in data.iloc[:, 6:].columns:
                res[col] = find_homogenous_course(data.dropna(subset=[col]), col)
                # print(f"{col}: {res[-1]}")
            plot_histograms(data)
            min_val = min(res.values())
            homogenous_course = [k for k, v in res.items() if v == min_val]
            print(f"with the test of Levene, we can determinated the most homogenous course:")
            print(f"{homogenous_course[0]} with : {min_val}")
            plot_histograms_homogenous(homogenous_course[0], data)
    except Exception as e:
        print(f"Error: {e}") 

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
