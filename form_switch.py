import random
import sys
from network import Switch
from PyQt6.QtGui import QIntValidator, QRegularExpressionValidator, QAction
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QSlider, QPushButton
from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal


class SwitchWindow(QMainWindow):
    switch_created = pyqtSignal(object)
    cancelled = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paramètrer le switch")
        self.resize(400, 300)
        self.is_validated = False

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
        for w in widgets:
            layout.addWidget(w)

    def validation(self):
        if not self.nom.text() or not self.ports.text():
            return

        print("Validé")
        sw = Switch(self.nom.text(), int(self.ports.text()))
        self.is_validated = True
        self.switch_created.emit(sw)
        print("Création du switch réussie")
        self.window().close()

    def closeEvent(self, event):
        if not self.is_validated:
            self.cancelled.emit()
        super().closeEvent(event)
