import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle


# -----------------------------
# TRENDLINE COMPUTATION
# -----------------------------
def compute_trendlines(candles):
    """
    Find upward trendlines touching two Low wicks.

    Rules:
      - Only bottom wicks (Low values) are used as touch points.
      - Line must angle upward: Low[B] > Low[A].
      - At least one candle must exist between A and B (B >= A + 2).
      - No candle between A and B may have its Low below the trendline
        at that index (line is not violated underneath between touch points).
      - After a line A→B is accepted, the next line's start point must
        be at index >= B (A cannot be reused as a start for another line).

    Returns a list of (i, j) index pairs for accepted trendlines.
    """
    n = len(candles)
    lows = [float(c["Low"]) for c in candles]

    lines = []       # accepted (A, B) pairs
    min_next_start = 0  # earliest index the next line's A can be

    # Walk through every possible A
    a = 0
    while a < n - 2:
        if a < min_next_start:
            a += 1
            continue

        nearest_b = None

        # Find the nearest valid B for this A (earliest legitimate trendline)
        for b in range(a + 2, n):
            low_a = lows[a]
            low_b = lows[b]

            # Must angle upward
            if low_b <= low_a:
                continue

            # Check no candle between A and B dips below the trendline
            slope = (low_b - low_a) / (b - a)
            valid = True
            for k in range(a + 1, b):
                line_price = low_a + slope * (k - a)
                if lows[k] < line_price:
                    valid = False
                    break

            if valid:
                nearest_b = b
                break  # take the earliest valid B, not the furthest

        if nearest_b is not None:
            lines.append((a, nearest_b))
            min_next_start = nearest_b  # next line's A must start at nearest_b or later
            a = nearest_b               # advance A past this line's B
        else:
            a += 1

    return lines


class CandleViewer(QMainWindow):
    def __init__(self, json_path):
        super().__init__()

        self.setWindowTitle("Candle Step Viewer")
        self.setGeometry(100, 100, 1200, 700)

        # -----------------------------
        # LOAD DATA
        # -----------------------------
        with open(json_path, "r") as f:
            self.candles = json.load(f)

        self.index = 0

        # -----------------------------
        # PRE-COMPUTE GLOBAL PRICE RANGE
        # -----------------------------
        all_prices = []
        for c in self.candles:
            all_prices.extend([
                float(c["Open"]),
                float(c["High"]),
                float(c["Low"]),
                float(c["Close"])
            ])

        self.global_min = min(all_prices)
        self.global_max = max(all_prices)

        # -----------------------------
        # PRE-COMPUTE ALL TRENDLINES
        # -----------------------------
        self.trendlines = compute_trendlines(self.candles)

        # -----------------------------
        # UI SETUP
        # -----------------------------
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        layout = QVBoxLayout(self.main_widget)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        # -----------------------------
        # FIX: PREVENT 0–1 AUTO SCALE ON START
        # -----------------------------
        self.ax.set_xlim(-1, len(self.candles) + 1)
        self.ax.set_ylim(self.global_min * 0.999, self.global_max * 1.001)
        self.ax.autoscale(False)

        self.draw_chart()

    # -----------------------------
    # KEYBOARD CONTROL
    # -----------------------------
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right:
            if self.index < len(self.candles):
                self.index += 1
                self.draw_chart()

        elif event.key() == Qt.Key_Left:
            if self.index > 0:
                self.index -= 1
                self.draw_chart()

    # -----------------------------
    # DRAW CANDLES
    # -----------------------------
    def draw_chart(self):
        self.ax.clear()

        visible = self.candles[:self.index]

        if not visible:
            self.canvas.draw()
            return

        lows = [float(c["Low"]) for c in self.candles]

        for i, c in enumerate(visible):
            o = float(c["Open"])
            h = float(c["High"])
            l = float(c["Low"])
            cl = float(c["Close"])

            color = "green" if cl >= o else "red"

            # wick
            self.ax.plot(
                [i, i],
                [l, h],
                color=color,
                linewidth=1
            )

            # body
            body_bottom = min(o, cl)
            body_height = abs(cl - o)

            rect = Rectangle(
                (i - 0.3, body_bottom),
                0.6,
                body_height if body_height != 0 else 0.001,
                color=color
            )
            self.ax.add_patch(rect)

        # -----------------------------
        # DRAW TRENDLINES
        # Trendline is visible only when both its touch points (A and B)
        # have been revealed. The line is extended rightward to the current
        # visible index so you can see it projecting forward.
        # -----------------------------
        for (a, b) in self.trendlines:
            # Both touch points must be visible
            if b >= self.index:
                continue

            low_a = lows[a]
            low_b = lows[b]
            slope = (low_b - low_a) / (b - a)

            # Extend line from A to the rightmost visible candle
            x_end = self.index - 1
            y_start = low_a
            y_end = low_a + slope * (x_end - a)

            self.ax.plot(
                [a, x_end],
                [y_start, y_end],
                color="dodgerblue",
                linewidth=1.5,
                linestyle="--",
                alpha=0.85,
                zorder=3
            )

            # Mark the two touch points with small dots
            self.ax.plot(
                [a, b],
                [low_a, low_b],
                "o",
                color="dodgerblue",
                markersize=4,
                zorder=4
            )

        # -----------------------------
        # FIXED AXIS (NO ZOOMING)
        # -----------------------------
        self.ax.set_xlim(-1, len(self.candles) + 1)
        self.ax.set_ylim(self.global_min * 0.999, self.global_max * 1.001)

        self.ax.set_title(f"Candles: {self.index}/{len(self.candles)}")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Price")

        self.canvas.draw()


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    file_path, _ = QFileDialog.getOpenFileName(
        None,
        "Select Candle JSON File",
        "",
        "JSON Files (*.json)"
    )

    if not file_path:
        print("No file selected.")
        sys.exit()

    window = CandleViewer(file_path)
    window.show()

    sys.exit(app.exec_())