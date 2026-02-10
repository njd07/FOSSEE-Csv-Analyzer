from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# matplotlib charts embedded in qt
class ChartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 4), facecolor='#1e1e2f')
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    # draw type distribution + averages
    def draw_charts(self, data):
        self.figure.clear()
        labels = data.get('labels', [])
        counts = data.get('counts', [])
        avgs = data.get('averages', {})

        # bar chart - type counts
        ax1 = self.figure.add_subplot(1, 2, 1)
        ax1.set_facecolor('#28293d')
        ax1.bar(labels, counts, color='#5a9cf5')
        ax1.set_title('Type Distribution', color='#ddd', fontsize=10)
        ax1.tick_params(colors='#aaa', labelsize=8)
        for s in ax1.spines.values(): s.set_color('#3a3a55')

        # bar chart - averages
        ax2 = self.figure.add_subplot(1, 2, 2)
        ax2.set_facecolor('#28293d')
        ax2.bar(list(avgs.keys()), list(avgs.values()), color='#e07c4f')
        ax2.set_title('Parameter Averages', color='#ddd', fontsize=10)
        ax2.tick_params(colors='#aaa', labelsize=8)
        for s in ax2.spines.values(): s.set_color('#3a3a55')

        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()
