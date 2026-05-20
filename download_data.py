import yfinance as yf
import os
import json

def download_stock_data(symbols, interval="1h", period="1mo"):
    folder_name = f"{interval}_{period}"
    base_path = os.path.join("data", folder_name)
    os.makedirs(base_path, exist_ok=True)

    for symbol in symbols:
        print(f"Downloading {symbol}...")

        data = yf.download(
            symbol,
            interval=interval,
            period=period,
            progress=False
        )

        if data.empty:
            print(f"⚠️ No data for {symbol}")
            continue

        # Flatten columns (removes tuple issue)
        data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

        # move datetime index into a column
        data = data.reset_index()

        json_data = data.to_dict(orient="records")

        file_path = os.path.join(base_path, f"{symbol}.json")

        with open(file_path, "w") as f:
            json.dump(json_data, f, indent=2, default=str)

        print(f"Saved -> {file_path}")


if __name__ == "__main__":
    symbols = ["AAPL", "MSFT", "TSLA"]

    interval = "4h"
    period = "3mo"

    download_stock_data(symbols, interval, period)
