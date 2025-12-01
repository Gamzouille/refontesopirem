import sys

from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QSlider, QPushButton
from PyQt6.QtCore import Qt, QRegularExpression


class SwitchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètrer le switch")
        self.resize(400, 300)

        # --- Contenu central ---
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        central.setLayout(layout)

        # --- Widgets ---
        self.nom = QLineEdit(parent=self)
        input_validator = QRegularExpressionValidator(
            QRegularExpression("[a-zA-Z0-9]+"), self.nom
        )
        self.nom.setValidator(input_validator)
        self.ports = QLineEdit(parent=self)
        self.ports.setValidator(QIntValidator(1, 8, self))

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.validation)

        widgets = [QLabel("Nom"), self.nom, QLabel("Nombre de ports"), self.ports, QLabel(""), self.valider]
        for w in widgets:
            w.show()

        # --- Placeholder ---
        label = QLabel(" ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #555;")
        for w in widgets:
            layout.addWidget(w)

    def validation(self):
        print("okok")