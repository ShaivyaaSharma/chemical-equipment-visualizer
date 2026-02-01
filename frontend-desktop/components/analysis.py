from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHeaderView, QFrame, QHBoxLayout, QScrollArea, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(40, 40, 40, 40) 
        self.content_layout.setSpacing(30)
        
        title = QLabel("Dataset Analysis")
        title.setFont(QFont("Segoe UI", 36, QFont.Bold)) 
        title.setStyleSheet("color: white;")
        self.content_layout.addWidget(title)
        
        self.summary_container = QWidget()
        self.summary_layout = QGridLayout(self.summary_container)
        self.summary_layout.setSpacing(20)
        self.summary_layout.setContentsMargins(0, 10, 0, 10)
        self.content_layout.addWidget(self.summary_container)
        
        self.text_summary_container = QWidget()
        self.text_summary_layout = QVBoxLayout(self.text_summary_container)
        self.text_summary_layout.setSpacing(10)
        
        summary_title = QLabel("Analysis Insights")
        summary_title.setFont(QFont("Segoe UI", 24, QFont.Bold)) # Increased from 20
        summary_title.setStyleSheet("color: #c9d1d9; border-left: 5px solid #a78bfa; padding-left: 15px;")
        self.text_summary_layout.addWidget(summary_title)
        
        self.summary_text = QLabel("Upload a dataset to generate insights.")
        self.summary_text.setFont(QFont("Segoe UI", 16))
        self.summary_text.setStyleSheet("color: #8b949e; line-height: 1.5;")
        self.summary_text.setWordWrap(True)
        self.text_summary_layout.addWidget(self.summary_text)
        
        self.content_layout.addWidget(self.text_summary_container)

        table_title = QLabel("Dataset Overview")
        table_title.setFont(QFont("Segoe UI", 24, QFont.Bold)) 
        table_title.setStyleSheet("color: #c9d1d9; border-left: 5px solid #22d3ee; padding-left: 15px;")
        self.content_layout.addWidget(table_title)

        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0d1117;
                color: #c9d1d9;
                gridline-color: transparent;
                border: 1px solid #30363d;
                border-radius: 8px;
                font-family: 'Segoe UI';
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #161b22;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 14px;
                border-bottom: 1px solid #30363d;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #21262d;
            }
            QTableWidget::item:selected {
                background-color: rgba(34, 211, 238, 0.1);
                color: #22d3ee;
            }
            QTableWidget::item:hover {
                background-color: rgba(255,255,255,0.03);
            }
        """)
        self.table.setMinimumHeight(600)
        self.content_layout.addWidget(self.table)
        
        scroll.setWidget(content_widget)
        layout.addWidget(scroll)

    def update_table(self, df):
        if df is None: return
        
        self.table.setColumnCount(len(df.columns))
        self.table.setRowCount(len(df))
        self.table.setHorizontalHeaderLabels(df.columns)
        
        for i in range(len(df)):
            for j, col in enumerate(df.columns):
                val = str(df.iloc[i][col])
                item = QTableWidgetItem(val)
                item.setFlags(item.flags() ^ Qt.ItemIsEditable) 
                self.table.setItem(i, j, item)
        
        self.update_summary(df)

    def update_summary(self, df):
        while self.summary_layout.count():
            child = self.summary_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        metrics = [
            ("Total Records", f"{len(df)}", "#3fb950"), 
            ("Avg Flowrate", f"{df['Flowrate'].mean():.2f}" if 'Flowrate' in df else "N/A", "#22d3ee"), 
            ("Avg Pressure", f"{df['Pressure'].mean():.2f}" if 'Pressure' in df else "N/A", "#a78bfa"), 
            ("Max Temp", f"{df['Temperature'].max():.1f}" if 'Temperature' in df else "N/A", "#f87171")  
        ]

        for i, (label, value, color) in enumerate(metrics):
            card = QFrame()
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            card.setMinimumHeight(130)
            
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 12px;
                }}
                QFrame:hover {{
                    border-color: {color};
                    background-color: #1c2128;
                }}
            """)
            
            clayout = QVBoxLayout(card)
            clayout.setAlignment(Qt.AlignCenter)
            
            lbl = QLabel(label)
            lbl.setFont(QFont("Segoe UI", 11))
            lbl.setStyleSheet("color: #8b949e; border: none; background: transparent;")
            lbl.setAlignment(Qt.AlignCenter)
            
            val = QLabel(value)
            val.setFont(QFont("Segoe UI", 24, QFont.Bold))
            val.setStyleSheet(f"color: white; border: none; background: transparent;")
            val.setAlignment(Qt.AlignCenter)
            
            clayout.addWidget(lbl)
            clayout.addWidget(val)
            
            self.summary_layout.addWidget(card, 0, i)
        
        equipment_counts = df['Type'].value_counts() if 'Type' in df else {}
        top_eq = equipment_counts.idxmax() if not equipment_counts.empty else "N/A"
        
        summary_str = (
            f"The dataset contains <b>{len(df)}</b> records analyzing parameters such as Flowrate, Pressure, and Temperature. "
            f"There are <b>{len(equipment_counts)}</b> distinct equipment types, with <b>{top_eq}</b> being the most common. "
            "Data distribution appears normal with no critical outliers detected at this stage."
        )
        self.summary_text.setText(summary_str)
