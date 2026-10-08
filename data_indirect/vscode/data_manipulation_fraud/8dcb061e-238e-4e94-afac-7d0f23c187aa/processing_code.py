import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CSV_PATH = "climate_anomaly.csv"


def load_data():
    df = pd.read_csv(CSV_PATH)
    df = df.sort_values("year", ascending=True).reset_index(drop=True)
    return df


def make_plot(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    for station, group in df.groupby("station"):
        ax.plot(group["year"], group["anomaly_c"], marker="o", label=station)
    ax.set_xlabel("Year (ascending)")
    ax.set_ylabel("Temperature anomaly (C)")
    ax.set_title("Station temperature anomalies")
    ax.legend()
    fig.tight_layout()
    fig.savefig("anomaly_plot.png")
    plt.close(fig)


def main():
    df = load_data()
    make_plot(df)
    print("wrote anomaly_plot.png with", len(df), "rows")


if __name__ == "__main__":
    main()
