from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

# equipment data table
class TableView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.label = QLabel("Equipment Data")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.label)
        self.table = QTableWidget()
        layout.addWidget(self.table)
        self.setLayout(layout)

    # fill table from list of dicts
    def load_rows(self, rows):
        if not rows:
            self.table.setRowCount(0)
            return
        cols = list(rows[0].keys())
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, col in enumerate(cols):
                self.table.setItem(i, j, QTableWidgetItem(str(row.get(col, ''))))
        self.table.resizeColumnsToContents()
