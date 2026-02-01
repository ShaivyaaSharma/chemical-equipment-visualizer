from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QColor
import datetime

class HistoryItemWidget(QWidget):
    def __init__(self, item_data, view_callback):
        super().__init__()
        self.item_data = item_data
        
        layout = QHBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        self.setLayout(layout)
        
        icon_box = QFrame()
        icon_box.setFixedSize(50, 50)
        icon_box.setStyleSheet("""
            background-color: rgba(255,255,255,0.05); 
            border-radius: 8px;
            image: url(frontend-desktop/assets/file-text.svg);
            padding: 10px;
        """)
        layout.addWidget(icon_box)
        
        text_layout = QVBoxLayout()
        text_layout.setSpacing(8)
        
        title = QLabel(item_data['name'])
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: white;")
        text_layout.addWidget(title)
        
        try:
            dt_str = item_data['uploaded_at'].split('T')[0]
            date_obj = datetime.datetime.strptime(dt_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m/%Y")
        except:
            formatted_date = item_data['uploaded_at'][:10] 
            
        meta_text = f"Uploaded {formatted_date} • {item_data.get('size', '2.4 MB')}"
        meta = QLabel(meta_text)
        meta.setFont(QFont("Segoe UI", 12))
        meta.setStyleSheet("color: #8b949e;")
        text_layout.addWidget(meta)
        
        summary = QLabel(item_data['summary'])
        summary.setFont(QFont("Segoe UI", 14)) 
        summary.setStyleSheet("color: #8b949e; line-height: 1.4;")
        summary.setWordWrap(True)
        text_layout.addWidget(summary)
        
        layout.addLayout(text_layout, 1) 
        
        badge = QLabel("ANALYZED")
        badge.setAlignment(Qt.AlignCenter)
        badge.setStyleSheet("""
            background-color: rgba(139, 92, 246, 0.15);
            color: #a78bfa;
            font-weight: bold;
            padding: 4px 10px;
            border-radius: 12px; 
            font-size: 10px; 
            min-width: 60px;
        """)
        layout.addWidget(badge, 0, Qt.AlignVCenter) 
        
        view_btn = QPushButton("View")
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: 1px solid rgba(255,255,255,0.2);
                color: white;
                padding: 6px 16px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: rgba(255,255,255,0.1);
                border-color: white;
            }
        """)
        view_btn.clicked.connect(lambda: view_callback(item_data['id']))
        layout.addWidget(view_btn, 0, Qt.AlignVCenter) 

class HistoryPage(QWidget):
    def __init__(self, load_dataset_callback):
        super().__init__()
        self.load_dataset_callback = load_dataset_callback
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("Recent History")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setStyleSheet("color: white; margin: 20px 0;")
        layout.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: #161b22;
                border: 1px solid #30363d;
                border-radius: 8px;
                margin-bottom: 15px;
            }
            QListWidget::item:hover {
                background-color: #1c2128;
                border-color: #58a6ff;
            }
        """)
        layout.addWidget(self.list_widget)

    def update_history(self, history_data):
        self.list_widget.clear()
        for item in history_data:
            list_item = QListWidgetItem(self.list_widget)
            list_item.setSizeHint(item_widget_size_hint()) 
            
            widget = HistoryItemWidget(item, self.load_dataset_callback)
            self.list_widget.setItemWidget(list_item, widget)

def item_widget_size_hint():
    from PyQt5.QtCore import QSize
    return QSize(0, 200) 
