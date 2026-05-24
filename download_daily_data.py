import yfinance as yf
import os
import json
import pandas as pd
from datetime import datetime, timedelta

def download_stock_data(symbols, start_date, end_date, interval="1m"):
    """
    Downloads stock data day-by-day between start_date and end_date (inclusive).
    
    start_date / end_date format: "YYYY-MM-DD"
    """

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    # Iterate day by day
    current_day = start_date

    while current_day <= end_date:
        next_day = current_day + timedelta(days=1)

        day_str = current_day.strftime("%d_%b")  # e.g. 26_May

        print(f"\n📅 Processing day: {day_str}")

        for symbol in symbols:
            print(f"  ⬇️ Downloading {symbol}...")

            # Download ONLY this day's data using start/end
            data = yf.download(
                symbol,
                interval=interval,
                start=current_day.strftime("%Y-%m-%d"),
                end=next_day.strftime("%Y-%m-%d"),
                progress=False,
            )

            if data.empty:
                print(f"  ⚠️ No data for {symbol} on {day_str}")
                continue

            # Flatten columns if needed
            data.columns = [
                col[0] if isinstance(col, tuple) else col for col in data.columns
            ]

            # Reset index
            data = data.reset_index()

            # Normalize datetime column name
            if "Datetime" not in data.columns:
                data.rename(columns={data.columns[0]: "Datetime"}, inplace=True)

            data["Datetime"] = pd.to_datetime(data["Datetime"])

            # Folder: data/{symbol}_1m/
            folder_name = f"{symbol}"
            base_path = os.path.join("data", f"daily_{interval}", folder_name)
            os.makedirs(base_path, exist_ok=True)

            # Save file per day
            file_path = os.path.join(base_path, f"{day_str}.json")

            json_data = data.to_dict(orient="records")

            with open(file_path, "w") as f:
                json.dump(json_data, f, indent=2, default=str)

            print(f"  💾 Saved -> {file_path}")

        current_day += timedelta(days=1)


if __name__ == "__main__":
    symbols = [
        "SHOP.TO",
        "CLS.TO",
        "ATD.TO",
        "BN.TO",
        "CJT.TO",
        "LSPD.TO",
        "CSU.TO",
        "WSP.TO",
        "IFC.TO",
        "GSY.TO",
        "EQB.TO",
        "CCO.TO",
        "NTR.TO",
        "CVE.TO",
        "TRI.TO",
        "OTEX.TO",
        "DOL.TO",
        "ENB.TO",
    ]

    interval = "1m"

    start_date = "2026-05-01"
    end_date = "2026-05-20"

    download_stock_data(symbols, start_date, end_date, interval)