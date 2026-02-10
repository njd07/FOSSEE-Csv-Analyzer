import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QLabel, QSplitter
)
from PyQt5.QtCore import Qt
from components.auth_dialog import AuthDialog
from components.table_view import TableView
from components.chart_view import ChartView

API = "http://localhost:8000/api"

# dark theme styles
DARK_STYLE = """
QMainWindow, QWidget { background: #1e1e2f; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
QPushButton { background: #3b6cb4; color: #fff; border: none; padding: 8px 16px; border-radius: 4px; }
QPushButton:hover { background: #5a9cf5; }
QPushButton:disabled { background: #555; }
QTableWidget { background: #28293d; color: #e0e0e0; gridline-color: #3a3a55; border: 1px solid #3a3a55; }
QHeaderView::section { background: #3b6cb4; color: #fff; padding: 4px; border: 1px solid #3a3a55; }
QLabel { color: #e0e0e0; }
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.token = None
        self.current_id = None
        self.setWindowTitle("CSV Visualizer")
        self.setMinimumSize(900, 600)
        self._build_ui()
        self._login()

    def _build_ui(self):
        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout()

        # top buttons
        top = QHBoxLayout()
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self._upload)
        top.addWidget(self.upload_btn)

        self.pdf_btn = QPushButton("Download PDF")
        self.pdf_btn.clicked.connect(self._download_pdf)
        self.pdf_btn.setEnabled(False)
        top.addWidget(self.pdf_btn)

        self.status = QLabel("Not logged in.")
        top.addWidget(self.status)
        top.addStretch()
        layout.addLayout(top)

        # table + chart split
        split = QSplitter(Qt.Vertical)
        self.table_view = TableView()
        split.addWidget(self.table_view)
        self.chart_view = ChartView()
        split.addWidget(self.chart_view)
        split.setSizes([300, 300])
        layout.addWidget(split)

        w.setLayout(layout)

    def _login(self):
        dlg = AuthDialog(API, self)
        if dlg.exec_() == AuthDialog.Accepted and dlg.token:
            self.token = dlg.token
            self.status.setText("Logged in.")
        else:
            self.status.setText("Not authenticated.")

    def _headers(self):
        return {"Authorization": f"Token {self.token}"}

    # upload csv file
    def _upload(self):
        if not self.token:
            QMessageBox.warning(self, "Error", "Login first.")
            return
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV (*.csv)")
        if not path:
            return
        self.status.setText("Uploading...")
        try:
            with open(path, 'rb') as f:
                r = requests.post(f"{API}/upload/", files={"file": f}, headers=self._headers(), timeout=30)
            if r.status_code == 201:
                data = r.json()
                self.current_id = data['id']
                self.status.setText(f"Uploaded: {data['name']}")
                self.pdf_btn.setEnabled(True)
                self._load_data(data['id'])
            else:
                QMessageBox.warning(self, "Failed", r.json().get('error', 'Error'))
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    # fetch and show chart data
    def _load_data(self, did):
        try:
            r = requests.get(f"{API}/chart-data/?id={did}", headers=self._headers(), timeout=10)
            if r.status_code == 200:
                d = r.json()
                self.table_view.load_rows(d.get('rows', []))
                self.chart_view.draw_charts(d)
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # save pdf to disk
    def _download_pdf(self):
        if not self.current_id:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Save PDF", f"report_{self.current_id}.pdf", "PDF (*.pdf)")
        if not path:
            return
        try:
            r = requests.get(f"{API}/report/?id={self.current_id}", headers=self._headers(), timeout=15)
            if r.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(r.content)
                QMessageBox.information(self, "Done", f"Saved to {path}")
            else:
                QMessageBox.warning(self, "Error", "Failed to get report.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(DARK_STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
