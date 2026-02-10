from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

class ChartView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(11, 5.5), facecolor='#0a0a0a', dpi=100)
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def draw_charts(self, data):
        self.figure.clear()
        labels = data.get('labels', [])
        counts = data.get('counts', [])
        avgs = data.get('averages', {})

        ax1 = self.figure.add_subplot(1, 2, 1, facecolor='#0a0a0a')
        
        x_pos = np.arange(len(labels))
        colors = plt.cm.RdYlBu_r(np.linspace(0.3, 0.8, len(labels)))
        
        bars = ax1.bar(x_pos, counts, color=colors, edgecolor='#60a5fa', 
                       linewidth=2.5, alpha=0.9, width=0.6)
        
        for idx, (bar, count) in enumerate(zip(bars, counts)):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + max(counts)*0.02,
                    f'{int(height)}',
                    ha='center', va='bottom', color='#60a5fa', 
                    fontsize=11, fontweight='bold')
            
            gradient = plt.cm.Blues(np.linspace(0.4, 0.9, 100))
            for i in range(100):
                h = height * i / 100
                ax1.barh(h, bar.get_width(), left=bar.get_x(), 
                        height=height/100, color=gradient[i], 
                        alpha=0.1, zorder=0)
        
        ax1.set_title('Equipment Type Distribution', 
                     color='#fafafa', fontsize=14, fontweight='bold', pad=20)
        ax1.set_xlabel('Equipment Type', color='#a3a3a3', fontsize=11, fontweight='500')
        ax1.set_ylabel('Count', color='#a3a3a3', fontsize=11, fontweight='500')
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(labels, rotation=15, ha='right')
        ax1.tick_params(colors='#a3a3a3', labelsize=10)
        ax1.grid(True, alpha=0.15, linestyle='--', linewidth=0.8, axis='y')
        ax1.set_ylim(0, max(counts) * 1.15 if counts else 10)
        
        for spine in ax1.spines.values():
            spine.set_color('#262626')
            spine.set_linewidth(2)
        
        ax2 = self.figure.add_subplot(1, 2, 2, projection='polar', facecolor='#0a0a0a')
        
        param_names = list(avgs.keys())
        param_values = list(avgs.values())
        
        if param_names and param_values:
            N = len(param_names)
            angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
            param_values_plot = param_values + [param_values[0]]
            angles_plot = angles + [angles[0]]
            
            ax2.plot(angles_plot, param_values_plot, 'o-', linewidth=3, 
                    color='#60a5fa', markersize=10, markerfacecolor='#3b82f6',
                    markeredgecolor='#fafafa', markeredgewidth=2, zorder=3)
            
            ax2.fill(angles_plot, param_values_plot, alpha=0.25, color='#3b82f6')
            ax2.fill(angles_plot, param_values_plot, alpha=0.15, color='#60a5fa')
            
            for angle, value, name in zip(angles, param_values, param_names):
                ax2.plot([angle, angle], [0, value], color='#262626', 
                        linewidth=1, alpha=0.3, linestyle='--')
            
            ax2.set_xticks(angles)
            ax2.set_xticklabels(param_names, color='#fafafa', fontsize=10, fontweight='500')
            ax2.tick_params(colors='#a3a3a3', labelsize=9, pad=10)
            ax2.set_title('Parameter Averages (Radar)', 
                         color='#fafafa', fontsize=14, fontweight='bold', y=1.1, pad=20)
            
            ax2.grid(True, alpha=0.25, linestyle='-', linewidth=1, color='#444')
            ax2.set_ylim(0, max(param_values) * 1.2 if param_values else 10)
            
            ax2.spines['polar'].set_color('#262626')
            ax2.spines['polar'].set_linewidth(2)

        self.figure.tight_layout(pad=3.0)
        self.canvas.draw()
