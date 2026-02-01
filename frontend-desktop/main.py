import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QStackedWidget
from components.auth import LoginPage, SignupPage
from components.main_window import MainContent
from components.styles import STYLES

class DesktopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1400, 900)
        self.user = None
        self.password = None

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        
        self.stack = QStackedWidget()
        self.layout.addWidget(self.stack)

        self.auth_container = QWidget()
        self.auth_stack = QStackedWidget()
        auth_layout = QVBoxLayout(self.auth_container)
        auth_layout.addWidget(self.auth_stack)
        
        self.login_page = LoginPage(self)
        self.signup_page = SignupPage(self)
        self.auth_stack.addWidget(self.login_page)
        self.auth_stack.addWidget(self.signup_page)
        
        self.main_content = MainContent(self)

        self.stack.addWidget(self.auth_container)
        self.stack.addWidget(self.main_content)
        
        self.show_auth_page("login")

    def show_auth_page(self, page_name):
        if page_name == "login":
            self.auth_stack.setCurrentWidget(self.login_page)
        else:
            self.auth_stack.setCurrentWidget(self.signup_page)

    def start_app_session(self):
        self.main_content.set_user(self.user)
        self.stack.setCurrentWidget(self.main_content)

    def logout(self):
        self.user = None
        self.password = None
        self.stack.setCurrentWidget(self.auth_container)
        self.show_auth_page("login")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLES)
    window = DesktopApp()
    window.show()
    sys.exit(app.exec_())
