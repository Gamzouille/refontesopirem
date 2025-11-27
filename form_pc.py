from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox
from PyQt6.QtCore import Qt

class PcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètrer le pc")
        self.resize(800, 600)

        # --- Contenu central ---
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        central.setLayout(layout)

        # --- Widgets ---
        widget = QComboBox()
        widget.addItems(["192.168.0.1", "192.168.0.2", "192.168.0.3"])
        widget.show()

        # --- Placeholder ---
        label = QLabel(" ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #555;")
        layout.addWidget(label)
