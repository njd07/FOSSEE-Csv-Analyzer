import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QMessageBox, QLabel, QSplitter, QComboBox
)
from PyQt5.QtCore import Qt
from components.auth_dialog import AuthDialog
from components.table_view import TableView
from components.chart_view import ChartView

API = "http://localhost:8000/api"


# Custom dark theme stylesheet
STYLE = """
QMainWindow, QWidget { 
    background: #0a0a0a; 
    color: #fafafa; 
    font-family: 'Segoe UI', sans-serif; 
}
QPushButton { 
    background: #3b82f6; 
    color: #fff; 
    border: none; 
    padding: 8px 16px; 
    border-radius: 6px; 
    font-weight: 600;
    margin: 2px;
}
QPushButton:hover { background: #2563eb; }
QPushButton:disabled { background: #525252; opacity: 0.6; }
QPushButton#deleteBtn { background: #dc2626; }
QPushButton#deleteBtn:hover { background: #b91c1c; }
QPushButton#logoutBtn { background: #525252; }
QPushButton#logoutBtn:hover { background: #404040; }
QTableWidget { 
    background: #171717; 
    color: #fafafa; 
    gridline-color: #333; 
    border: 1px solid #333; 
    selection-background-color: #3b82f6;
}
QHeaderView::section { 
    background: #262626; 
    color: #fff; 
    padding: 8px; 
    border: 1px solid #333; 
    font-weight: 600;
}
QLabel { color: #a3a3a3; font-weight: 500; }
QComboBox {
    background: #171717;
    color: #fafafa;
    border: 1px solid #333;
    border-radius: 6px;
    padding: 6px 12px;
    min-width: 200px;
}
QComboBox:hover { border-color: #3b82f6; }
QComboBox::drop-down { border: none; }
QComboBox QAbstractItemView {
    background: #171717;
    color: #fafafa;
    selection-background-color: #3b82f6;
    border: 1px solid #333;
}
QSplitter::handle { background: #262626; }
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.token = None
        self.current_id = None
        self.history = []
        self.setWindowTitle("CSV Visualizer - Python (PyQt5)")
        self.setMinimumSize(1100, 700)
        self._build_ui()
        self._login()

    def _build_ui(self):
        # Creates the main window layout with buttons and charts
        w = QWidget()
        self.setCentralWidget(w)
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        top = QHBoxLayout()
        top.setSpacing(10)
        
        self.upload_btn = QPushButton("☁ Upload CSV")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self._upload)
        top.addWidget(self.upload_btn)

        self.pdf_btn = QPushButton("📄 Download PDF")
        self.pdf_btn.setCursor(Qt.PointingHandCursor)
        self.pdf_btn.clicked.connect(self._download_pdf)
        self.pdf_btn.setEnabled(False)
        top.addWidget(self.pdf_btn)

        self.dataset_combo = QComboBox()
        self.dataset_combo.setCursor(Qt.PointingHandCursor)
        self.dataset_combo.addItem("No datasets")
        self.dataset_combo.currentIndexChanged.connect(self._on_dataset_selected)
        self.dataset_combo.setEnabled(False)
        top.addWidget(QLabel("Dataset:"))
        top.addWidget(self.dataset_combo)

        self.delete_btn = QPushButton("🗑 Delete")
        self.delete_btn.setObjectName("deleteBtn")
        self.delete_btn.setCursor(Qt.PointingHandCursor)
        self.delete_btn.clicked.connect(self._delete_dataset)
        self.delete_btn.setEnabled(False)
        top.addWidget(self.delete_btn)

        top.addStretch()

        self.status = QLabel("Not logged in")
        self.status.setStyleSheet("color: #60a5fa;")
        top.addWidget(self.status)

        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("logoutBtn")
        self.logout_btn.setCursor(Qt.PointingHandCursor)
        self.logout_btn.clicked.connect(self._logout)
        self.logout_btn.setEnabled(False)
        top.addWidget(self.logout_btn)

        layout.addLayout(top)

        split = QSplitter(Qt.Vertical)
        self.table_view = TableView()
        split.addWidget(self.table_view)
        self.chart_view = ChartView()
        split.addWidget(self.chart_view)
        split.setSizes([350, 350])
        layout.addWidget(split)

        w.setLayout(layout)

    def _login(self):
        # Opens authentication dialog
        dlg = AuthDialog(API, self)
        if dlg.exec_() == AuthDialog.Accepted and dlg.token:
            self.token = dlg.token
            self.status.setText("Logged in")
            self.logout_btn.setEnabled(True)
            self._load_history()
        else:
            self.status.setText("Not authenticated")

    def _logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.token = None
            self.current_id = None
            self.history = []
            self.dataset_combo.clear()
            self.dataset_combo.addItem("No datasets")
            self.dataset_combo.setEnabled(False)
            self.pdf_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.logout_btn.setEnabled(False)
            self.table_view.load_rows([])
            self.chart_view.figure.clear()
            self.chart_view.canvas.draw()
            self.status.setText("Logged out")
            self._login()

    def _headers(self):
        return {"Authorization": f"Token {self.token}"}

    def _load_history(self):
        if not self.token:
            return
        try:
            r = requests.get(f"{API}/history/", headers=self._headers(), timeout=10)
            if r.status_code == 200:
                self.history = r.json()
                self.dataset_combo.blockSignals(True)
                self.dataset_combo.clear()
                self.dataset_combo.blockSignals(False)
                
                if self.history:
                    for ds in self.history:
                        self.dataset_combo.addItem(f"{ds['name']} ({ds['row_count']} rows)", ds['id'])
                    self.dataset_combo.setEnabled(True)
                    self.dataset_combo.setCurrentIndex(0) # Select first by default
                else:
                    self.dataset_combo.addItem("No datasets")
                    self.dataset_combo.setEnabled(False)
                    self.current_id = None
                    self.delete_btn.setEnabled(False)
                    self.pdf_btn.setEnabled(False)
        except Exception as e:
            print(f"Failed to load history: {e}")

    def _on_dataset_selected(self, index):
        if index >= 0 and self.dataset_combo.count() > 0:
            dataset_id = self.dataset_combo.itemData(index)
            if dataset_id:
                self.current_id = dataset_id
                self.pdf_btn.setEnabled(True)
                self.delete_btn.setEnabled(True)
                self._load_data(dataset_id)

    def _upload(self):
        # Handles file upload to server
        if not self.token:
            QMessageBox.warning(self, "Error", "Login first")
            return
        path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV (*.csv)")
        if not path:
            return
        self.status.setText("Uploading...")
        QApplication.processEvents()
        try:
            with open(path, 'rb') as f:
                r = requests.post(f"{API}/upload/", files={"file": f}, headers=self._headers(), timeout=30)
            if r.status_code == 201:
                data = r.json()
                self.status.setText(f"Uploaded: {data['name']}")
                self._load_history()
                # Select the new item
                count = self.dataset_combo.count()
                for i in range(count):
                    if self.dataset_combo.itemData(i) == data['id']:
                        self.dataset_combo.setCurrentIndex(i)
                        break
            else:
                QMessageBox.warning(self, "Failed", r.json().get('error', 'Error'))
                self.status.setText("Upload failed")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            self.status.setText("Upload error")

    def _delete_dataset(self):
        # Deletes the currently selected dataset
        if not self.current_id:
            return
        reply = QMessageBox.question(self, 'Delete', 'Are you sure you want to delete this dataset?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                r = requests.delete(f"{API}/delete/{self.current_id}/", headers=self._headers(), timeout=10)
                if r.status_code == 200:
                    self.status.setText("Dataset deleted")
                    self.table_view.load_rows([])
                    self.chart_view.figure.clear()
                    self.chart_view.canvas.draw()
                    self._load_history()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete dataset")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def _load_data(self, did):
        try:
            r = requests.get(f"{API}/chart-data/?id={did}", headers=self._headers(), timeout=10)
            if r.status_code == 200:
                d = r.json()
                self.table_view.load_rows(d.get('rows', []))
                self.chart_view.draw_charts(d)
                self.status.setText(f"Loaded dataset #{did}")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

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
                QMessageBox.warning(self, "Error", "Failed to get report")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
