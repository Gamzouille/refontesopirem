from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt

class ProjectWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nouveau projet - Sopirem")
        self.resize(800, 600)

        # --- Contenu central ---
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        central.setLayout(layout)

        # --- Placeholder ---
        label = QLabel("Page de nouveau projet (vide pour l’instant)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #555;")
        layout.addWidget(label)