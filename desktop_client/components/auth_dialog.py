from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import requests

class AuthDialog(QDialog):
    def __init__(self, api_base, parent=None):
        super().__init__(parent)
        self.api_base = api_base
        self.token = None
        self.setWindowTitle("Login")
        self.setFixedSize(300, 180)
        self._setup()

    def _setup(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Username:"))
        self.user_input = QLineEdit()
        layout.addWidget(self.user_input)

        layout.addWidget(QLabel("Password:"))
        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pass_input)

        btn = QPushButton("Login")
        btn.clicked.connect(self._login)
        layout.addWidget(btn)
        self.setLayout(layout)

    def _login(self):
        u = self.user_input.text().strip()
        p = self.pass_input.text().strip()
        if not u or not p:
            QMessageBox.warning(self, "Error", "Fill both fields")
            return
        try:
            r = requests.post(f"{self.api_base}/auth/token/", json={"username": u, "password": p}, timeout=10)
            if r.status_code == 200:
                self.token = r.json().get("token")
                self.accept()
            else:
                QMessageBox.warning(self, "Failed", "Bad credentials")
        except requests.RequestException as e:
            QMessageBox.critical(self, "Error", str(e))
