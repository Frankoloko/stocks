import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle


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

        for i, c in enumerate(visible):
            o = float(c["Open"])
            h = float(c["High"])
            l = float(c["Low"])
            cl = float(c["Close"])

            color = "green" if cl >= o else "red"

            # wick (same color as candle)
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