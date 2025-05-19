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
    '''Show the histogram by features'''
    houses = data["Hogwarts House"].unique()
    features = [col for col in data.columns if col not in ["Index", "Hogwarts House", "First Name", "Last Name", "Birthday", "Best Hand"]]
    house_colors = {
        "Gryffindor": "#740001",
        "Hufflepuff": "#EEBA35",
        "Ravenclaw": "#0F1D4A", 
        "Slytherin": "#1A472A" 
    }
    for feature in features:
        plt.figure(figsize=(10, 6))
        for house in houses:
            house_data = data[data["Hogwarts House"] == house][feature]
            house_data = house_data.dropna()
            plt.hist(house_data, alpha=0.6, bins=20, label=house, color=house_colors.get(house, 'pink'))

        plt.title(f"Histogram of {feature} by House")
        plt.xlabel("Score")
        plt.ylabel("Number of Students")
        plt.legend()
        plt.grid(True)
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
    main()