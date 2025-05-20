import pandas as pd
import matplotlib.pyplot as plt
import sys
import os


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


def scatter_plot(data):
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