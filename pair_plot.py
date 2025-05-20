import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
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


def main():
    try:
        assert len(sys.argv) == 2, "Invalid number of parameters"
        data: pd.DataFrame = load(sys.argv[1])

        house_col = 'Hogwarts House'
        assert house_col in data.columns, f"Missing column '{house_col}' in data"

        columns = data.columns[6:]
        subset = data[columns].copy()
        subset[house_col] = data[house_col]

        g = sns.pairplot(subset,
                            hue=house_col,
                            diag_kind="hist",
                            corner=False,
                            palette=house_colors,
                            plot_kws={"alpha": 0.8, "s": 5})

        fig = g.fig

        # Create map: ax -> (x_col, y_col)
        axes_map = {}
        for i, y_col in enumerate(columns):
            for j, x_col in enumerate(columns):
                if i == j:
                    continue  # ignore diag (histograms)
                try:
                    ax = g.axes[i, j]
                    axes_map[ax] = (x_col, y_col)
                except IndexError:
                    continue

        fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, axes_map, subset, house_col))
        plt.show()

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("\ninteruption...\nbye!!!\n")
        exit(1)
