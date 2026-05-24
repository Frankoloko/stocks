import os
import json
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt


# ============================================
# CONFIG
# ============================================

DATA_FOLDER = r"C:\Francois\repos\stocks\data\1m_8d"

START_BALANCE = 1000.0

# Market open
MARKET_OPEN_HOUR = 9
MARKET_OPEN_MINUTE = 30

# First 30 min range ends
RANGE_END_HOUR = 10
RANGE_END_MINUTE = 0


# ============================================
# LOAD JSON
# ============================================

def load_json_to_df(file_path):

    with open(file_path, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Normalize columns
    df.columns = [c.lower() for c in df.columns]

    # Datetime
    df["datetime"] = pd.to_datetime(df["datetime"], utc=True)

    # Convert timezone
    df["datetime"] = df["datetime"].dt.tz_convert("America/New_York")

    # Sort
    df = df.sort_values("datetime").reset_index(drop=True)

    return df


# ============================================
# STRATEGY
# ============================================

def run_strategy(df):

    balance = START_BALANCE

    trades = []

    total_trades = 0
    wins = 0
    losses = 0

    # ----------------------------------------
    # Group by day
    # ----------------------------------------

    df["date"] = df["datetime"].dt.date

    grouped = df.groupby("date")

    # ========================================
    # LOOP DAYS
    # ========================================

    for date, day_df in grouped:

        day_df = day_df.reset_index(drop=True)

        # ----------------------------------------
        # Opening range
        # ----------------------------------------

        opening_range = day_df[
            (
                (day_df["datetime"].dt.hour > MARKET_OPEN_HOUR)
                |
                (
                    (day_df["datetime"].dt.hour == MARKET_OPEN_HOUR)
                    &
                    (day_df["datetime"].dt.minute >= MARKET_OPEN_MINUTE)
                )
            )
            &
            (
                (day_df["datetime"].dt.hour < RANGE_END_HOUR)
                |
                (
                    (day_df["datetime"].dt.hour == RANGE_END_HOUR)
                    &
                    (day_df["datetime"].dt.minute == RANGE_END_MINUTE)
                )
            )
        ]

        if opening_range.empty:
            continue

        opening_high = opening_range["high"].max()
        opening_low = opening_range["low"].min()

        range_size = opening_high - opening_low

        if range_size <= 0:
            continue

        # ----------------------------------------
        # After opening range
        # ----------------------------------------

        after_range = day_df[
            (
                (day_df["datetime"].dt.hour > RANGE_END_HOUR)
                |
                (
                    (day_df["datetime"].dt.hour == RANGE_END_HOUR)
                    &
                    (day_df["datetime"].dt.minute > RANGE_END_MINUTE)
                )
            )
        ]

        in_trade = False

        # ONLY ONE TRADE PER DAY
        trade_taken_today = False

        # ========================================
        # LOOP CANDLES
        # ========================================

        for i, row in after_range.iterrows():

            high = row["high"]
            low = row["low"]

            # ====================================
            # ENTRY
            # ====================================

            if not in_trade and not trade_taken_today:

                # Break above opening range high
                if high > opening_high:

                    entry_price = opening_high

                    # Stop loss halfway back into range
                    stop_loss = opening_high - (range_size * 0.5)

                    # Risk per share
                    risk = entry_price - stop_loss

                    # 2R target
                    take_profit = entry_price + (risk * 4)

                    # Use full account balance
                    shares = balance / entry_price

                    in_trade = True
                    trade_taken_today = True

                    total_trades += 1

                    entry_time = row["datetime"]

            # ====================================
            # MANAGE TRADE
            # ====================================

            elif in_trade:

                hit_stop = low <= stop_loss
                hit_target = high >= take_profit

                exit_price = None
                result = None

                # If both happen same candle
                # assume stop hits first
                if hit_stop and hit_target:
                    exit_price = stop_loss
                    result = "LOSS"

                elif hit_stop:
                    exit_price = stop_loss
                    result = "LOSS"

                elif hit_target:
                    exit_price = take_profit
                    result = "WIN"

                # --------------------------------
                # CLOSE TRADE
                # --------------------------------

                if exit_price is not None:

                    pnl = (exit_price - entry_price) * shares

                    balance += pnl

                    if result == "WIN":
                        wins += 1
                    else:
                        losses += 1

                    trades.append({
                        "entry_time": entry_time,
                        "exit_time": row["datetime"],
                        "entry_price": entry_price,
                        "exit_price": exit_price,
                        "result": result,
                        "balance": balance,
                    })

                    in_trade = False

        # ====================================
        # FORCE CLOSE END OF DAY
        # ====================================

        if in_trade:

            last_row = day_df.iloc[-1]

            last_close = last_row["close"]

            pnl = (last_close - entry_price) * shares

            balance += pnl

            if last_close > entry_price:
                wins += 1
                result = "WIN"
            else:
                losses += 1
                result = "LOSS"

            trades.append({
                "entry_time": entry_time,
                "exit_time": last_row["datetime"],
                "entry_price": entry_price,
                "exit_price": last_close,
                "result": result,
                "balance": balance,
            })

    # ========================================
    # FINAL STATS
    # ========================================

    success_rate = 0

    if total_trades > 0:
        success_rate = (wins / total_trades) * 100

    return {
        "final_balance": round(balance, 2),
        "return_pct": round(((balance - START_BALANCE) / START_BALANCE) * 100, 2),
        "total_trades": total_trades,
        "wins": wins,
        "losses": losses,
        "success_rate": round(success_rate, 2),
        "trades": trades,
    }


# ============================================
# EXPORT CHART
# ============================================

def export_chart(df, trades, output_path):

    chart_df = df.copy()

    chart_df = chart_df.set_index("datetime")

    # ----------------------------------------
    # Marker arrays
    # ----------------------------------------

    buy_markers = pd.Series(index=chart_df.index, dtype=float)
    sell_markers = pd.Series(index=chart_df.index, dtype=float)

    for trade in trades:

        entry_time = trade["entry_time"]
        exit_time = trade["exit_time"]

        if entry_time in chart_df.index:
            buy_markers.loc[entry_time] = trade["entry_price"]

        if exit_time in chart_df.index:
            sell_markers.loc[exit_time] = trade["exit_price"]

    # ----------------------------------------
    # Plot markers
    # ----------------------------------------

    apds = []

    # Buy arrows
    apds.append(
        mpf.make_addplot(
            buy_markers,
            type="scatter",
            marker="^",
            markersize=100,
        )
    )

    # Sell arrows
    apds.append(
        mpf.make_addplot(
            sell_markers,
            type="scatter",
            marker="v",
            markersize=100,
        )
    )

    # ----------------------------------------
    # Create chart
    # ----------------------------------------

    fig, axlist = mpf.plot(
        chart_df,
        type="candle",
        style="charles",
        volume=False,
        addplot=apds,
        figsize=(18, 10),
        title=os.path.basename(output_path),
        returnfig=True,
    )

    # ----------------------------------------
    # Save image
    # ----------------------------------------

    fig.savefig(
        output_path,
        dpi=200,
        bbox_inches="tight"
    )

    plt.close(fig)


# ============================================
# MAIN
# ============================================

def main():

    results = []

    for file_name in os.listdir(DATA_FOLDER):

        if not file_name.endswith(".json"):
            continue

        file_path = os.path.join(DATA_FOLDER, file_name)

        print(f"Running: {file_name}")

        try:

            # ------------------------------------
            # LOAD
            # ------------------------------------

            df = load_json_to_df(file_path)

            # ------------------------------------
            # RUN STRATEGY
            # ------------------------------------

            stats = run_strategy(df)

            results.append({
                "symbol": file_name.replace(".json", ""),
                **stats
            })

            # ------------------------------------
            # EXPORT IMAGE
            # ------------------------------------

            image_path = os.path.join(
                DATA_FOLDER,
                file_name.replace(".json", ".png")
            )

            export_chart(
                df,
                stats["trades"],
                image_path
            )

            print(f"Saved chart: {image_path}")

        except Exception as e:

            print(f"ERROR: {file_name}")
            print(e)

    # ========================================
    # FINAL RESULTS
    # ========================================

    print("\n" + "=" * 110)
    print("FINAL RESULTS")
    print("=" * 110)

    results = sorted(
        results,
        key=lambda x: x["final_balance"],
        reverse=True
    )

    for r in results:

        print(
            f"{r['symbol']:15} | "
            f"Balance: ${r['final_balance']:10.2f} | "
            f"Return: {r['return_pct']:8.2f}% | "
            f"Trades: {r['total_trades']:4} | "
            f"Win Rate: {r['success_rate']:6.2f}%"
        )


# ============================================
# ENTRY
# ============================================

if __name__ == "__main__":
    main()