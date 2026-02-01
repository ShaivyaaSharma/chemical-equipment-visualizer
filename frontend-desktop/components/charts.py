from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QLabel, QFrame, QHBoxLayout, QComboBox, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('dark_background')

class ChartCard(QFrame):
    def __init__(self, title, chart_types=None, on_change=None):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 12px;
            }
            QFrame:hover {
                border-color: #58a6ff;
            }
        """)
        self.setMinimumHeight(600) 
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(25, 25, 25, 25)
        
        header_layout = QHBoxLayout()
        
        title_lbl = QLabel(title)
        title_lbl.setFont(QFont("Segoe UI", 20, QFont.Bold)) 
        title_lbl.setStyleSheet("color: #f0f6fc; border: none; background: transparent;")
        header_layout.addWidget(title_lbl)
        
        header_layout.addStretch()
        
        self.combo = QComboBox()
        self.combo.setCursor(Qt.PointingHandCursor)
        self.combo.setStyleSheet("""
            QComboBox {
                background-color: #0d1117;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 6px; 
                padding: 6px 15px; 
                min-width: 140px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QComboBox:hover { 
                border-color: #8b949e; 
                background-color: #161b22;
            }
            QComboBox::drop-down { 
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
                image: url(frontend-desktop/assets/chevron-down.svg);
            }
            QComboBox QAbstractItemView {
                background-color: #161b22;
                color: white;
                selection-background-color: #1f6feb;
                border: 1px solid #30363d;
                outline: none;
            }
        """)
        if chart_types:
            self.combo.addItems(chart_types)
            self.combo.currentTextChanged.connect(on_change)
            header_layout.addWidget(self.combo)
        
        self.layout.addLayout(header_layout)
        
        self.canvas = None
        self.layout.addStretch() 

    def plot(self, figure):
        if self.canvas:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()
        
        self.canvas = FigureCanvas(figure)
        self.canvas.setStyleSheet("background: transparent; border: none;")
        self.layout.insertWidget(1, self.canvas)
        self.layout.setStretch(1, 1)

class ChartsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.df = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(40, 40, 40, 40)
        self.content_layout.setSpacing(50) 
        
        header = QLabel("Equipment Analytics")
        header.setFont(QFont("Segoe UI", 32, QFont.Bold))
        header.setStyleSheet("color: white; margin-bottom: 20px;")
        self.content_layout.addWidget(header)

        self.flow_card = ChartCard("Flowrate Analysis", ["Bar Chart", "Line Chart", "Histogram"], lambda t: self.update_flow_chart(t))
        self.temp_card = ChartCard("Temperature Trends", ["Line Chart", "Bar Chart", "Histogram"], lambda t: self.update_temp_chart(t))
        self.press_card = ChartCard("Pressure Analysis", ["Bar Chart", "Line Chart"], lambda t: self.update_press_chart(t))
        self.dist_card = ChartCard("Equipment Type Distribution", ["Pie Chart", "Doughnut Chart", "Bar Chart"], lambda t: self.update_dist_chart(t))
        
        self.content_layout.addWidget(self.flow_card)
        self.content_layout.addWidget(self.temp_card)
        self.content_layout.addWidget(self.press_card)
        self.content_layout.addWidget(self.dist_card)
        
        scroll.setWidget(content)
        layout.addWidget(scroll)

    def update_charts(self, df):
        if df is None: return
        self.df = df
        self.update_flow_chart(self.flow_card.combo.currentText())
        self.update_temp_chart(self.temp_card.combo.currentText())
        self.update_press_chart(self.press_card.combo.currentText())
        self.update_dist_chart(self.dist_card.combo.currentText())

    def _get_common_fig(self):
        fig = Figure(figsize=(10, 6), facecolor='#161b22')
        ax = fig.add_subplot(111)
        ax.set_facecolor('#161b22')
        ax.grid(color='#30363d', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.tick_params(axis='both', colors='#8b949e', labelsize=8) 
        for spine in ax.spines.values(): spine.set_color('#30363d')
        return fig, ax

    def update_flow_chart(self, chart_type):
        if self.df is None: return
        fig, ax = self._get_common_fig()
        names = self.df["Equipment Name"]
        data = self.df["Flowrate"]

        if chart_type == "Bar Chart":
            ax.bar(names, data, color='#22d3ee', alpha=0.8, edgecolor='#22d3ee')
        elif chart_type == "Line Chart":
            ax.plot(names, data, color='#22d3ee', marker='o', linewidth=2, markersize=6)
            ax.fill_between(names, data, color='#22d3ee', alpha=0.1)
        elif chart_type == "Histogram":
            ax.hist(data, bins=10, color='#22d3ee', alpha=0.7, edgecolor='#161b22')
        
        if chart_type != "Histogram":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
        else:
             plt.setp(ax.get_xticklabels(), fontsize=7)
        
        fig.tight_layout()
        self.flow_card.plot(fig)

    def update_temp_chart(self, chart_type):
        if self.df is None: return
        fig, ax = self._get_common_fig()
        names = self.df["Equipment Name"]
        data = self.df["Temperature"]

        color = '#f87171' 
        if chart_type == "Line Chart":
            ax.plot(names, data, color=color, marker='o', linewidth=3)
            ax.fill_between(names, data, color=color, alpha=0.15)
        elif chart_type == "Bar Chart":
            ax.bar(names, data, color=color, alpha=0.8)
        elif chart_type == "Histogram":
            ax.hist(data, bins=10, color=color, alpha=0.7, edgecolor='#161b22')

        if chart_type != "Histogram":
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
        else:
             plt.setp(ax.get_xticklabels(), fontsize=7)
            
        fig.tight_layout()
        self.temp_card.plot(fig)

    def update_press_chart(self, chart_type):
        if self.df is None: return
        fig, ax = self._get_common_fig()
        names = self.df["Equipment Name"]
        data = self.df["Pressure"]
        
        color = '#a78bfa'
        if chart_type == "Bar Chart":
            ax.bar(names, data, color=color, alpha=0.8)
        elif chart_type == "Line Chart":
            ax.plot(names, data, color=color, marker='o', linewidth=2)
            ax.fill_between(names, data, color=color, alpha=0.1)
            
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
        fig.tight_layout()
        self.press_card.plot(fig)

    def update_dist_chart(self, chart_type):
        if self.df is None: return
        counts = self.df["Type"].value_counts()
        
        if chart_type == "Bar Chart":
            fig, ax = self._get_common_fig()
            ax.bar(counts.index, counts.values, color='#36A2EB')
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=7)
            self.dist_card.plot(fig)
            return

        fig = Figure(figsize=(10, 6), facecolor='#161b22')
        ax = fig.add_subplot(111)
        colors = ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0', '#9966FF']
        wedgeprops = {'edgecolor': '#161b22', 'linewidth': 2}
        if chart_type == "Doughnut Chart":
            wedgeprops['width'] = 0.4
            
        wedges, texts, autotexts = ax.pie(
            counts.values, 
            labels=None, 
            autopct='%1.1f%%', 
            pctdistance=0.85 if chart_type == "Doughnut Chart" else 0.6,
            colors=colors, 
            textprops={'color': 'white', 'fontsize': 10, 'fontweight': 'bold'}, 
            wedgeprops=wedgeprops,
            startangle=90
        )
        
        ax.legend(wedges, counts.index, title="Equipment Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
        
        fig.tight_layout()
        self.dist_card.plot(fig)
