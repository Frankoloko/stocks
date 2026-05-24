import json
import os

# ── Configuration ─────────────────────────────────────────────────────────────

DATA_FOLDER    = r"C:\Francois\repos\stocks\data\1h_1mo"
STARTING_CAPITAL = 1000.0

# ─────────────────────────────────────────────────────────────────────────────


def compute_mas(closes, period):
    mas = []
    for i in range(len(closes)):
        if i < period - 1:
            mas.append(None)
        else:
            mas.append(sum(closes[i - period + 1:i + 1]) / period)
    return mas


def run_backtest(json_path):
    with open(json_path) as f:
        candles = json.load(f)

    closes = [float(c['Close']) for c in candles]
    dates  = [c['Datetime'] for c in candles]
    ma5    = compute_mas(closes, 5)
    ma50   = compute_mas(closes, 50)

    capital  = STARTING_CAPITAL
    shares   = 0.0
    in_trade = False

    for i in range(1, len(closes)):
        if ma5[i] is None or ma50[i] is None:
            continue
        if ma5[i-1] is None or ma50[i-1] is None:
            continue

        was_above = ma5[i-1] > ma50[i-1]
        is_above  = ma5[i]   > ma50[i]
        price     = closes[i]
        date      = dates[i][:16]

        if not in_trade and not was_above and is_above:
            shares   = capital / price
            capital  = 0.0
            in_trade = True
            print(f"  BUY  — {date}  |  price: ${price:>8.2f}  |  shares: {shares:.4f}")

        elif in_trade and was_above and not is_above:
            capital  = shares * price
            shares   = 0.0
            in_trade = False
            print(f"  SELL — {date}  |  price: ${price:>8.2f}  |  portfolio: ${capital:,.2f}")

    if in_trade:
        final_price = closes[-1]
        final_date  = dates[-1][:16]
        capital     = shares * final_price
        print(f"  SELL — {final_date}  |  price: ${final_price:>8.2f}  |  portfolio: ${capital:,.2f}  (open — valued at last candle)")

    return_pct = ((capital - STARTING_CAPITAL) / STARTING_CAPITAL) * 100
    return capital, return_pct


def main():
    json_files = sorted([
        f for f in os.listdir(DATA_FOLDER) if f.endswith('.json')
    ])

    if not json_files:
        print(f"No JSON files found in: {DATA_FOLDER}")
        return

    results = []

    for filename in json_files:
        ticker = os.path.splitext(filename)[0]
        path   = os.path.join(DATA_FOLDER, filename)

        print(f"\n{'─' * 60}")
        print(f"  {ticker}")
        print(f"{'─' * 60}")

        try:
            final_value, return_pct = run_backtest(path)
            print(f"\n  Final value: ${final_value:,.2f}  ({return_pct:+.2f}%)")
            results.append((ticker, final_value, return_pct))
        except Exception as e:
            print(f"  ERROR: {e}")

    if not results:
        return

    # ── Summary ───────────────────────────────────────────────────────────────
    results.sort(key=lambda r: r[2], reverse=True)

    print(f"\n{'═' * 60}")
    print(f"  RESULTS SUMMARY  (starting capital: ${STARTING_CAPITAL:,.2f})")
    print(f"{'═' * 60}")
    for rank, (ticker, value, pct) in enumerate(results, 1):
        bar = '█' * max(0, int(pct / 2))
        print(f"  {rank:>2}. {ticker:<10}  ${value:>8,.2f}  ({pct:>+7.2f}%)  {bar}")

    best = results[0]
    print(f"\n  🏆 Best performer: {best[0]}  —  ${best[1]:,.2f}  ({best[2]:+.2f}%)")


if __name__ == "__main__":
    main()