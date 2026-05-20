import os
import json
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt


def load_json_to_df(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Try to normalize column names (handles different formats)
    df.columns = [col.lower() for col in df.columns]

    # Identify datetime column
    if "datetime" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime"])
        df.set_index("datetime", inplace=True)
    elif "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df.set_index("date", inplace=True)

    # Ensure correct ordering
    df = df.sort_index()

    # mplfinance requires these exact columns
    df = df[["open", "high", "low", "close"]]

    return df


def create_candlestick_chart(df, output_path, title):
    fig, axlist = mpf.plot(
        df,
        type="candle",
        style="charles",
        title=title,
        volume=False,
        figsize=(16, 8),
        returnfig=True,
    )

    # ✅ THIS is the important part
    fig.savefig(
        output_path,
        dpi=300,              # high resolution here
        bbox_inches="tight"
    )

    plt.close(fig)


def process_folder(base_folder="data"):
    for folder in os.listdir(base_folder):
        folder_path = os.path.join(base_folder, folder)

        if not os.path.isdir(folder_path):
            continue

        output_folder = os.path.join(folder_path)
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(folder_path):
            if not file.endswith(".json"):
                continue

            file_path = os.path.join(folder_path, file)
            symbol = file.replace(".json", "")

            print(f"Processing {symbol}...")

            try:
                df = load_json_to_df(file_path)

                output_path = os.path.join(output_folder, f"{symbol}.png")

                create_candlestick_chart(df, output_path, symbol)

                print(f"Saved chart -> {output_path}")

            except Exception as e:
                print(f"Failed {symbol}: {e}")


if __name__ == "__main__":
    process_folder()