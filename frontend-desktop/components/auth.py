from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QFrame, QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QCursor
import requests

API_BASE = "http://127.0.0.1:8000/api"

AUTH_BG = "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #000000, stop:0.5 #211e44, stop:1 #000000);"

class LoginPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setStyleSheet(AUTH_BG)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        container = QFrame()
        container.setFixedWidth(400)
        container.setStyleSheet("background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px;")
        
        clayout = QVBoxLayout(container)
        clayout.setSpacing(15)

        title = QLabel("Login")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background: transparent; color: white;")
        clayout.addWidget(title)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.user_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.user_in)

        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)
        self.pass_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.pass_in)

        login_btn = QPushButton("Sign In")
        login_btn.setProperty("class", "primary")
        login_btn.setCursor(QCursor(Qt.PointingHandCursor))
        login_btn.setStyleSheet("""
            QPushButton { background-color: #238636; color: white; border-radius: 6px; padding: 10px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #2ea043; }
        """)
        login_btn.clicked.connect(self.handle_login)
        clayout.addWidget(login_btn)

        signup_link = QPushButton("Need an account? Sign up")
        signup_link.setFlat(True)
        signup_link.setStyleSheet("color: #22d3ee; text-decoration: underline; background: transparent; border: none;")
        signup_link.setCursor(QCursor(Qt.PointingHandCursor))
        signup_link.clicked.connect(lambda: self.main_app.show_auth_page("signup"))
        clayout.addWidget(signup_link)

        layout.addWidget(container)

    def handle_login(self):
        username = self.user_in.text()
        password = self.pass_in.text()
        
        try:
            res = requests.post(f"{API_BASE}/login/", json={"username": username, "password": password}, timeout=5)
            if res.status_code == 200:
                self.main_app.user = username
                self.main_app.password = password 
                self.main_app.start_app_session()
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {e}")

class SignupPage(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app
        self.setStyleSheet(AUTH_BG)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        self.setLayout(layout)

        container = QFrame()
        container.setFixedWidth(400)
        container.setStyleSheet("background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px;")
        clayout = QVBoxLayout(container)
        clayout.setSpacing(15)

        title = QLabel("Create Account")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("background: transparent; color: white;")
        clayout.addWidget(title)

        self.fullname_in = QLineEdit()
        self.fullname_in.setPlaceholderText("Full Name")
        self.fullname_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.fullname_in)

        self.user_in = QLineEdit()
        self.user_in.setPlaceholderText("Username")
        self.user_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.user_in)

        self.pass_in = QLineEdit()
        self.pass_in.setPlaceholderText("Password")
        self.pass_in.setEchoMode(QLineEdit.Password)
        self.pass_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.pass_in)

        self.conf_pass_in = QLineEdit()
        self.conf_pass_in.setPlaceholderText("Confirm Password")
        self.conf_pass_in.setEchoMode(QLineEdit.Password)
        self.conf_pass_in.setStyleSheet("background: #0d1117; color: white; border: 1px solid #30363d; padding: 10px; border-radius: 6px;")
        clayout.addWidget(self.conf_pass_in)

        signup_btn = QPushButton("Sign Up")
        signup_btn.setProperty("class", "primary")
        signup_btn.setCursor(QCursor(Qt.PointingHandCursor))
        signup_btn.setStyleSheet("""
            QPushButton { background-color: #238636; color: white; border-radius: 6px; padding: 10px; font-weight: bold; border: none; }
            QPushButton:hover { background-color: #2ea043; }
        """)
        signup_btn.clicked.connect(self.handle_signup)
        clayout.addWidget(signup_btn)

        login_link = QPushButton("Already have an account? Login")
        login_link.setFlat(True)
        login_link.setStyleSheet("color: #22d3ee; text-decoration: underline; background: transparent; border: none;")
        login_link.setCursor(QCursor(Qt.PointingHandCursor))
        login_link.clicked.connect(lambda: self.main_app.show_auth_page("login"))
        clayout.addWidget(login_link)

        layout.addWidget(container)

    def handle_signup(self):
        full_name = self.fullname_in.text()
        username = self.user_in.text()
        password = self.pass_in.text()
        confirm = self.conf_pass_in.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Username and Password are required.")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        try:
            res = requests.post(f"{API_BASE}/signup/", json={
                "username": username, 
                "password": password,
                "full_name": full_name
            }, timeout=5)
            
            if res.status_code == 201:
                QMessageBox.information(self, "Success", "Account created! Please login.")
                self.main_app.show_auth_page("login")
            else:
                try:
                    err_msg = res.json().get('error', res.text)
                except:
                    err_msg = res.text
                QMessageBox.warning(self, "Failed", f"Signup failed: {err_msg}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Connection error: {e}")
