from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton, QStackedWidget, QMessageBox, QFrame
)
from PyQt5.QtGui import QFont, QCursor, QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
import requests
import pandas as pd
import os

from .dashboard import DashboardPage
from .analysis import AnalysisPage
from .charts import ChartsPage
from .reports import ReportsPage
from .history import HistoryPage

API_BASE = "http://127.0.0.1:8000/api"

class MainContent(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.dataset_id = None
        self.df = None
        self.sidebar_icons_path = os.path.join("frontend-desktop", "assets", "icons")
        
        self.init_ui()

    def get_auth(self):
        return (self.main_app.user, self.main_app.password)

    def init_ui(self):
        root_layout = QVBoxLayout()
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        self.setLayout(root_layout)
        self.header = QWidget()
        self.header.setFixedHeight(90) 
        self.header.setStyleSheet("background: rgba(13, 17, 23, 0.98); border-bottom: 1px solid #30363d;")
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(30, 0, 30, 0)
        
        logo_label = QLabel()
        logo_path = os.path.join("frontend-web", "public", "logo.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            logo_label.setPixmap(pixmap.scaled(55, 55, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(logo_label)
        header_layout.addSpacing(20)

        title_lbl = QLabel("Chemical Equipment Parameter Visualizer")
        title_lbl.setFont(QFont("Segoe UI", 20, QFont.Bold)) 
        title_lbl.setStyleSheet("color: transparent; background-image: linear-gradient(to right, #00e676, #2979ff); -webkit-background-clip: text; color: #22d3ee;")
        header_layout.addWidget(title_lbl)
        
        header_layout.addStretch()

        self.user_lbl = QLabel(f"Welcome, {self.main_app.user}" if hasattr(self.main_app, 'user') else "User")
        self.user_lbl.setFont(QFont("Segoe UI", 12))
        self.user_lbl.setStyleSheet("color: #c9d1d9; font-weight: 600;")
        header_layout.addWidget(self.user_lbl)
        
        header_layout.addSpacing(20)

        logout_btn = QPushButton("Logout")
        logout_btn.setStyleSheet("""
            QPushButton {
                background: rgba(239, 68, 68, 0.1); 
                border: 1px solid rgba(239, 68, 68, 0.3);
                color: #f87171;
                padding: 10px 24px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background: rgba(239, 68, 68, 0.2);
                color: white;
                border-color: #ef4444;
            }
        """)
        logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        logout_btn.clicked.connect(self.main_app.logout)
        header_layout.addWidget(logout_btn)

        root_layout.addWidget(self.header)

        body_widget = QWidget()
        body_layout = QHBoxLayout(body_widget)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(300) 
        self.sidebar.setStyleSheet("background-color: rgba(13, 17, 23, 0.6); border-right: 1px solid #30363d;")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(15, 30, 15, 30)
        
        self.nav_list = QListWidget()
        self.nav_list.setFocusPolicy(Qt.NoFocus)
        self.nav_list.setIconSize(QSize(26, 26))
        
        nav_items = ["Dashboard", "Analysis", "Charts", "Reports", "History"]
        for name in nav_items:
            item = QListWidgetItem(f"   {name}")
            item.setSizeHint(QSize(0, 60)) 
            item.setData(Qt.UserRole, name.lower())
            
            icon_path = os.path.join(self.sidebar_icons_path, f"{name.lower()}.svg")
            if os.path.exists(icon_path):
                item.setIcon(QIcon(icon_path))
                
            self.nav_list.addItem(item)

        self.nav_list.setCurrentRow(0)
        self.nav_list.currentRowChanged.connect(self.change_page)
        sidebar_layout.addWidget(self.nav_list)
        
        sidebar_layout.addStretch()
        
        body_layout.addWidget(self.sidebar)

        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")
        
        self.dashboard_page = DashboardPage(self)
        self.analysis_page = AnalysisPage()
        self.charts_page = ChartsPage()
        self.reports_page = ReportsPage(self)
        self.history_page = HistoryPage(self.load_dataset)
        
        self.content_stack.addWidget(self.dashboard_page)
        self.content_stack.addWidget(self.analysis_page)
        self.content_stack.addWidget(self.charts_page)
        self.content_stack.addWidget(self.reports_page)
        self.content_stack.addWidget(self.history_page)
        
        body_layout.addWidget(self.content_stack)
        
        root_layout.addWidget(body_widget)
        
        self.update_sidebar_icons()

    def set_user(self, username):
        self.user_lbl.setText(f"Welcome, {username}")
        self.refresh_history()

    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        self.update_sidebar_icons()
        if index == 4:
            self.refresh_history()

    def update_sidebar_icons(self):
        selected_row = self.nav_list.currentRow()
        for i in range(self.nav_list.count()):
            item = self.nav_list.item(i)
            key = item.data(Qt.UserRole)
            suffix = "_active" if i == selected_row else ""
            icon_path = os.path.join(self.sidebar_icons_path, f"{key}{suffix}.svg")
            if os.path.exists(icon_path):
                item.setIcon(QIcon(icon_path))

    def navigate_to(self, index):
        self.nav_list.setCurrentRow(index)

    def refresh_history(self):
        try:
            auth = self.get_auth()
            res = requests.get(f"{API_BASE}/datasets/", auth=auth, timeout=5)
            if res.status_code == 200:
                data = res.json()
                self.history_page.update_history(data)
                self.dashboard_page.update_recent(data)
        except: pass

    def load_history_item(self, item):
        did = item.data(32)
        self.load_dataset(did)

    def load_dataset(self, dataset_id):
        self.dataset_id = dataset_id
        try:
            auth = self.get_auth()
            res = requests.get(f"{API_BASE}/dataset/{dataset_id}/data/", auth=auth, timeout=5)
            if res.status_code == 200:
                self.df = pd.DataFrame(res.json().get('data', []))
                self.analysis_page.update_table(self.df)
                self.charts_page.update_charts(self.df)
                self.reports_page.update_report(self.df, dataset_id)
                self.navigate_to(1)
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
