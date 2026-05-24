import os
import json
import pandas as pd


# =========================================================
# CONFIG
# =========================================================

JSON_FOLDER = r"C:\Francois\repos\stocks\data\4h_1mo"

STARTING_BALANCE = 1000.0
TRADING_FEE = 0.0

MIN_STREAK = 1
MAX_STREAK = 10
MIN_TRADES = 20

OUTPUT_CSV = "all_strategy_results.csv"


# =========================================================
# HELPERS
# =========================================================

def is_green(row):
    return row["Close"] > row["Open"]

def is_red(row):
    return row["Close"] < row["Open"]


# =========================================================
# STRATEGY TEST (LONG ONLY)
# =========================================================

def test_strategy(df, streak_count, streak_color):
    """
    Long-only strategy:
    - If streak condition is met:
        BUY at next candle open
        SELL at same candle close
    """

    balance = STARTING_BALANCE

    wins = 0
    losses = 0
    trades = 0

    for i in range(streak_count, len(df)):

        # -------------------------------------------------
        # CHECK STREAK CONDITION
        # -------------------------------------------------
        valid = True

        for j in range(i - streak_count, i):
            candle = df.iloc[j]

            if streak_color == "red" and not is_red(candle):
                valid = False
                break

            if streak_color == "green" and not is_green(candle):
                valid = False
                break

        if not valid:
            continue

        # -------------------------------------------------
        # EXECUTE LONG TRADE
        # -------------------------------------------------
        candle = df.iloc[i]

        open_price = candle["Open"]
        close_price = candle["Close"]

        if open_price <= 0:
            continue

        # LONG PnL
        pct_change = (close_price - open_price) / open_price

        balance *= (1 + pct_change)
        balance -= TRADING_FEE

        trades += 1

        if pct_change > 0:
            wins += 1
        else:
            losses += 1

    if trades == 0:
        return None

    return {
        "Trades": trades,
        "Wins": wins,
        "Losses": losses,
        "Win Rate %": round((wins / trades) * 100, 2),
        "Final Balance": round(balance, 2),
        "Return %": round(((balance - STARTING_BALANCE) / STARTING_BALANCE) * 100, 2),
    }


# =========================================================
# MAIN LOOP
# =========================================================

all_results = []

files = [f for f in os.listdir(JSON_FOLDER) if f.endswith(".json")]

print(f"Found {len(files)} files")

for file_name in files:

    path = os.path.join(JSON_FOLDER, file_name)

    print(f"Processing {file_name}")

    try:
        with open(path, "r") as f:
            data = json.load(f)

        df = pd.DataFrame(data)

        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df = df.sort_values("Datetime").reset_index(drop=True)

        for streak in range(MIN_STREAK, MAX_STREAK + 1):

            for streak_color in ["red", "green"]:

                result = test_strategy(df, streak, streak_color)

                if result is None:
                    continue

                if result["Trades"] < MIN_TRADES:
                    continue

                all_results.append({
                    "Symbol": file_name.replace(".json", ""),
                    "Strategy": f"{streak} {streak_color} candles -> LONG",
                    **result
                })

    except Exception as e:
        print(f"Error on {file_name}: {e}")


# =========================================================
# RESULTS
# =========================================================

results_df = pd.DataFrame(all_results)

if results_df.empty:
    print("No results")
    exit()

results_df = results_df.sort_values("Final Balance", ascending=False)

print("\nTOP STRATEGIES (LONG ONLY)\n")
print(results_df.head(50).to_string(index=False))


# =========================================================
# OVERALL STRATEGY PERFORMANCE
# =========================================================

overall = (
    results_df
    .groupby("Strategy")
    .agg({
        "Trades": "sum",
        "Wins": "sum",
        "Losses": "sum",
        "Final Balance": "mean",
        "Return %": "mean",
    })
    .reset_index()
)

overall["Win Rate %"] = (overall["Wins"] / overall["Trades"]) * 100
overall = overall.sort_values("Final Balance", ascending=False)

print("\nBEST OVERALL STRATEGIES (LONG ONLY)\n")
print(overall.to_string(index=False))


best = overall.iloc[0]

print("\nBEST STRATEGY\n")
print(best)


# =========================================================
# SAVE
# =========================================================

results_df.to_csv(OUTPUT_CSV, index=False)
overall.to_csv("overall_long_only.csv", index=False)

print("\nSaved results.")