import pandas as pd

def load_data(filepath):
    data = pd.read_csv(filepath)
    return data

if __name__ == "__main__":
    df = load_data("data/emails.csv")
    print(df.head())