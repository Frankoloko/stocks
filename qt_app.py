import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle


def compute_mas(closes, period):
    """Simple moving average. Returns list of None (warmup) then floats."""
    mas = []
    for i in range(len(closes)):
        if i < period - 1:
            mas.append(None)
        else:
            mas.append(sum(closes[i - period + 1:i + 1]) / period)
    return mas


def compute_trades(closes, ma5, ma50):
    """
    Buy  when ma5 crosses above ma50 (was below, now above).
    Sell when ma5 crosses back below ma50 (was above, now below).
    """
    trades = []
    in_trade = False
    entry_idx = None

    for i in range(1, len(closes)):
        if ma5[i] is None or ma50[i] is None:
            continue
        if ma5[i - 1] is None or ma50[i - 1] is None:
            continue

        was_above = ma5[i - 1] > ma50[i - 1]
        is_above  = ma5[i]     > ma50[i]

        if not in_trade and not was_above and is_above:
            # Golden cross — buy
            in_trade  = True
            entry_idx = i

        elif in_trade and was_above and not is_above:
            # Death cross — sell
            trades.append({'entry': entry_idx, 'exit': i})
            in_trade  = False
            entry_idx = None

    # Close any open trade at last candle
    if in_trade:
        trades.append({'entry': entry_idx, 'exit': len(closes) - 1, 'open': True})

    return trades


class CandleViewer(QMainWindow):
    def __init__(self, json_path):
        super().__init__()
        self.setWindowTitle("MA5 / MA50 Crossover")
        self.setGeometry(100, 100, 1400, 750)

        with open(json_path) as f:
            self.candles = json.load(f)

        self.n      = len(self.candles)
        self.index  = 0

        self.opens  = [float(c["Open"])  for c in self.candles]
        self.highs  = [float(c["High"])  for c in self.candles]
        self.lows   = [float(c["Low"])   for c in self.candles]
        self.closes = [float(c["Close"]) for c in self.candles]

        self.ma5  = compute_mas(self.closes, 5)
        self.ma50 = compute_mas(self.closes, 50)
        self.trades = compute_trades(self.closes, self.ma5, self.ma50)

        all_prices = self.opens + self.highs + self.lows + self.closes
        self.global_min = min(all_prices)
        self.global_max = max(all_prices)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        self.fig, self.ax = plt.subplots(figsize=(14, 7))
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.ax.set_xlim(-1, self.n + 1)
        self.ax.set_ylim(self.global_min * 0.998, self.global_max * 1.002)
        self.ax.autoscale(False)

        self.draw_chart()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right and self.index < self.n:
            self.index += 1
            self.draw_chart()
        elif event.key() == Qt.Key_Left and self.index > 0:
            self.index -= 1
            self.draw_chart()

    def draw_chart(self):
        self.ax.clear()

        price_range  = self.global_max - self.global_min
        arrow_offset = price_range * 0.012

        # ── Candles ──────────────────────────────────────────────────────────
        for i in range(self.index):
            o  = self.opens[i]
            h  = self.highs[i]
            l  = self.lows[i]
            cl = self.closes[i]
            color = "#26a69a" if cl >= o else "#ef5350"

            self.ax.plot([i, i], [l, h], color=color, linewidth=1, zorder=2)
            body_h = abs(cl - o) or 0.001
            self.ax.add_patch(Rectangle(
                (i - 0.3, min(o, cl)), 0.6, body_h, color=color, zorder=2
            ))

        # ── MA lines ─────────────────────────────────────────────────────────
        xs5,  ys5  = [], []
        xs50, ys50 = [], []
        for i in range(self.index):
            if self.ma5[i] is not None:
                xs5.append(i);  ys5.append(self.ma5[i])
            if self.ma50[i] is not None:
                xs50.append(i); ys50.append(self.ma50[i])

        if xs5:
            self.ax.plot(xs5,  ys5,  color='#FFD600', linewidth=1.4,
                         zorder=3, label='MA 5')
        if xs50:
            self.ax.plot(xs50, ys50, color='#42A5F5', linewidth=1.8,
                         zorder=3, label='MA 50')

        # ── Trades ───────────────────────────────────────────────────────────
        for trade in self.trades:
            entry = trade['entry']
            exit_ = trade['exit']
            is_open = trade.get('open', False)

            if entry >= self.index:
                continue

            # Entry arrow
            ep = self.closes[entry]
            self.ax.annotate(
                '▲ BUY',
                xy=(entry, ep - arrow_offset),
                xytext=(entry, ep - arrow_offset * 3.5),
                fontsize=7.5, color='#00E676', fontweight='bold',
                ha='center', va='top',
                arrowprops=dict(arrowstyle='->', color='#00E676', lw=1.5),
                zorder=5
            )

            # Exit arrow (only once the exit candle is visible)
            if exit_ < self.index:
                xp    = self.closes[exit_]
                label = '▼ HOLD' if is_open else '▼ SELL'
                color = '#aaaaaa' if is_open else '#FFD600'
                self.ax.annotate(
                    label,
                    xy=(exit_, xp + arrow_offset),
                    xytext=(exit_, xp + arrow_offset * 3.5),
                    fontsize=7.5, color=color, fontweight='bold',
                    ha='center', va='bottom',
                    arrowprops=dict(arrowstyle='->', color=color, lw=1.5),
                    zorder=5
                )

        # ── Axis / style ──────────────────────────────────────────────────────
        self.ax.set_xlim(-1, self.n + 1)
        self.ax.set_ylim(self.global_min * 0.998, self.global_max * 1.002)
        self.ax.set_title(
            f"MA5 × MA50 Crossover — Candle {self.index}/{self.n}  (← → to step)",
            fontsize=11
        )
        self.ax.set_xlabel("Candle Index")
        self.ax.set_ylabel("Price")
        self.ax.set_facecolor('#0d1117')
        self.fig.patch.set_facecolor('#0d1117')
        self.ax.tick_params(colors='#aaaaaa')
        self.ax.xaxis.label.set_color('#aaaaaa')
        self.ax.yaxis.label.set_color('#aaaaaa')
        self.ax.title.set_color('#dddddd')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#333333')

        handles = [
            mpatches.Patch(color='#FFD600', label='MA 5'),
            mpatches.Patch(color='#42A5F5', label='MA 50'),
            mpatches.Patch(color='#00E676', label='Buy (MA5 crosses above MA50)'),
            mpatches.Patch(color='#FFD600', label='Sell (MA5 crosses below MA50)'),
        ]
        self.ax.legend(handles=handles, loc='upper left', fontsize=8,
                       facecolor='#1a1a2e', edgecolor='#444',
                       labelcolor='#cccccc')

        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_path, _ = QFileDialog.getOpenFileName(
        None, "Select Candle JSON File", "", "JSON Files (*.json)"
    )
    if not file_path:
        print("No file selected.")
        sys.exit()

    window = CandleViewer(file_path)
    window.show()
    sys.exit(app.exec_())