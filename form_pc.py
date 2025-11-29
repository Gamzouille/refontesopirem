from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit
from PyQt6.QtCore import Qt

class PcWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètrer le pc")
        self.resize(400, 300)

        # --- Contenu central ---
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        central.setLayout(layout)

        # --- Widgets ---
        widgets = [QLabel("Nom"), QLineEdit(), QLabel("Adresse IP"), QLineEdit(), QLabel("Adresse MAC"), QLineEdit()]
        for w in widgets:
            w.show()

        # --- Placeholder ---
        label = QLabel(" ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #555;")
        for w in widgets:
            layout.addWidget(w)
