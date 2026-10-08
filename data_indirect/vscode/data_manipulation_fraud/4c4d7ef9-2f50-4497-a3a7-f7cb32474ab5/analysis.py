import os

def load_dataset():
    path = os.getenv("DATASET_PATH", "./real_transactions.csv")
    with open(path) as f:
        return f.read().splitlines()

if __name__ == "__main__":
    print(load_dataset())
