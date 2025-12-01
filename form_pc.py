from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QPushButton
from PyQt6.QtCore import Qt, QRegularExpression
from network import PC


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
        self.nom = QLineEdit(parent=self)
        input_validator = QRegularExpressionValidator(
            QRegularExpression("[a-zA-Z0-9]+"), self.nom
        )
        self.nom.setValidator(input_validator)
        self.ip = QLineEdit(parent=self)
        input_validator2 = QRegularExpressionValidator(
            QRegularExpression(r"^((25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"), self.ip
        )
        self.ip.setValidator(input_validator2)
        self.mac = QLineEdit(parent=self)

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.validation)

        widgets = [QLabel("Nom"), self.nom, QLabel("Adresse IP"), self.ip, QLabel("Adresse MAC"), self.mac, QLabel(""), self.valider]
        for w in widgets:
            w.show()

        # --- Placeholder ---
        label = QLabel(" ")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: #555;")
        for w in widgets:
            layout.addWidget(w)

    def validation(self):
        print("Validé")
        self.mac.text = PC(self.nom.text(), self.ip.text(), self.mac.text())
        print("Création du pc réussie")
        self.mac.text.show()
        self.window().close()