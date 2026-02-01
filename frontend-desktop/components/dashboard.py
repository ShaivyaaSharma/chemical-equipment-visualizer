from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QCursor, QDragEnterEvent, QDropEvent, QIcon, QPixmap
import requests
import os

API_BASE = "http://127.0.0.1:8000/api"

class ClickableDropArea(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.dashboard = parent

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files:
            self.dashboard.upload_file(files[0])

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dashboard.open_file_dialog()

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)
        self.setLayout(layout)

        center_layout = QHBoxLayout()
        center_layout.addStretch()

        card = ClickableDropArea(self)
        card.setFixedSize(600, 400)
        card.setStyleSheet("""
            QFrame {
                background-color: #161b22; 
                border: 1px solid #30363d; 
                border-radius: 12px;
            }
            QFrame:hover {
                border-color: #58a6ff;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(20)

        title = QLabel("Upload Dataset")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        title.setStyleSheet("color: white; border: none; background: transparent;")
        title.setAlignment(Qt.AlignLeft)
        
        drop_zone = QFrame()
        drop_zone.setFixedSize(500, 250)
        drop_zone.setStyleSheet("""
            background: rgba(255, 255, 255, 0.02);
            border: 2px dashed #30363d;
            border-radius: 8px;
        """)
        
        dz_layout = QVBoxLayout(drop_zone)
        dz_layout.setAlignment(Qt.AlignCenter)
        dz_layout.setSpacing(10)

        icon_lbl = QLabel()
        icon_path = os.path.join("frontend-desktop", "assets", "icons", "upload.svg")
        if os.path.exists(icon_path):
            pixmap = QIcon(icon_path).pixmap(QSize(64, 64))
            icon_lbl.setPixmap(pixmap)
        icon_lbl.setStyleSheet("border: none; background: transparent;")
        icon_lbl.setAlignment(Qt.AlignCenter)
        dz_layout.addWidget(icon_lbl)

        main_text = QLabel("Click to upload CSV")
        main_text.setFont(QFont("Segoe UI", 12, QFont.Bold))
        main_text.setStyleSheet("color: white; border: none; background: transparent;")
        main_text.setAlignment(Qt.AlignCenter)
        dz_layout.addWidget(main_text)

        sub_text = QLabel("or drag and drop file here")
        sub_text.setFont(QFont("Segoe UI", 10))
        sub_text.setStyleSheet("color: #8b949e; border: none; background: transparent;")
        sub_text.setAlignment(Qt.AlignCenter)
        dz_layout.addWidget(sub_text)

        limit_text = QLabel("Supports .csv, .xlsx (Max 50MB)")
        limit_text.setFont(QFont("Segoe UI", 9))
        limit_text.setStyleSheet("color: #484f58; border: none; background: transparent;")
        limit_text.setAlignment(Qt.AlignCenter)
        dz_layout.addWidget(limit_text)

        card_layout.addWidget(title)
        card_layout.addWidget(drop_zone)
        
        center_layout.addWidget(card)
        center_layout.addStretch()
        
        layout.addLayout(center_layout)

        recent_lbl = QLabel("Recent Activity")
        recent_lbl.setFont(QFont("Segoe UI", 12, QFont.Bold))
        recent_lbl.setStyleSheet("color: #c9d1d9; margin-top: 20px;")
        layout.addWidget(recent_lbl)

        self.recent_list = QListWidget()
        self.recent_list.setFixedHeight(150)
        self.recent_list.setStyleSheet("""
            QListWidget { background: transparent; border: none; }
            QListWidget::item { padding: 8px; color: #8b949e; border-bottom: 1px solid #30363d; }
            QListWidget::item:hover { color: white; background: rgba(255,255,255,0.05); }
        """)
        self.recent_list.itemClicked.connect(self.main_window.load_history_item)
        layout.addWidget(self.recent_list)

        layout.addStretch()

    def open_file_dialog(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open Dataset", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if fname:
            self.upload_file(fname)

    def upload_file(self, filepath):
        try:
            auth = self.main_window.get_auth()
            files = {'file': open(filepath, 'rb')}
            res = requests.post(f"{API_BASE}/upload-csv/", files=files, auth=auth, timeout=10)
            
            if res.status_code == 201:
                QMessageBox.information(self, "Success", "Dataset uploaded successfully!")
                self.main_window.refresh_history()
            else:
                QMessageBox.warning(self, "Failed", f"Upload failed: {res.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {e}")

    def update_recent(self, data):
        self.recent_list.clear()
        for d in data[:5]:
            item = QListWidgetItem(f"📄 {d['name']}  —  {d['uploaded_at'][:10]}")
            item.setData(32, d['id'])
            self.recent_list.addItem(item)
