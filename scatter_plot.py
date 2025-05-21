import pandas as pd
import matplotlib.pyplot as plt
import sys
import os
from utils import load


house_colors = {
    "Gryffindor": "#740001",
    "Hufflepuff": "#EEBA35",
    "Ravenclaw": "#0F1D4A", 
    "Slytherin": "#1A472A" 
}


def on_click(event, axes_map, data, house_col='Hogwarts House'):
    ax = event.inaxes
    if ax is None:
        return

    try:
        key = axes_map.get(ax)
        if not key:
            return

        x_col, y_col = key

        # plot graph
        fig, ax = plt.subplots(figsize=(8, 6))
        for house, group in data.groupby(house_col):
            color = house_colors.get(house, None)
            ax.scatter(group[x_col],
                        group[y_col],
                        label=house,
                        color=color,
                        alpha=0.8,
                        s=60)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{y_col} vs {x_col}")
        ax.legend()
        plt.show()

    except Exception as e:
        print(f"on_click error: {e}")



def scatter_plot(data):
    try:
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
        axes_map = {}

        
        for i, ax in enumerate(axes):
            if i >= len(features):
                ax.axis('off')
                continue
            x_col = i 
            y_col = features[i]
            axes_map[ax] = (x_col, y_col)

            for house, group in data.groupby("Hogwarts House"):
                ax.scatter(group[x_col], group[y_col],
                           label=house,
                           color=house_colors.get(house, "gray"),
                           alpha=0.7,
                           s=40)
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            ax.set_title(f"{y_col} vs {x_col}")
            ax.legend()
        plt.grid(True)
        plt.tight_layout()
        fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, axes_map, subset, house_col))
        plt.show()



    except Exception as e:
        print(f"Error: {e}")
    

def main():
    assert len(sys.argv) == 2, "Usage: python scatter_plot.py dataset_train.csv"

    data = load(sys.argv[1])
    if data is not None:
        scatter_plot(data)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\n bye\n")
        exit(1)