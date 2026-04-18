from PyQt6.QtGui import QRegularExpressionValidator, QIntValidator
from PyQt6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QComboBox, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import Qt, QRegularExpression, pyqtSignal
import random
from core.devices.pc import PC


def generate_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

class PcWindow(QMainWindow):
    pc_created = pyqtSignal(object)

    def __init__(self, ip_conflict_checker=None):
        super().__init__()
        self.setWindowTitle("Paramètrer le pc")
        self.resize(400, 300)
        self.ip_conflict_checker = ip_conflict_checker

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
        self.mac = QLabel(generate_mac())

        self.valider = QPushButton("Valider")
        self.valider.clicked.connect(self.validation)

        widgets = [QLabel("Nom"), self.nom, QLabel("Adresse IP"), self.ip, QLabel("Adresse MAC"), self.mac, QLabel(""), self.valider]
        #for w in widgets:
        #    w.show()

        # --- Placeholder ---
        for w in widgets:
            layout.addWidget(w)

    def validation(self):
        nom = self.nom.text().strip()
        ip = self.ip.text().strip()

        if not nom:
            QMessageBox.warning(self, "Champ requis", "Le nom du PC ne peut pas être vide.")
            return

        if not self.nom.hasAcceptableInput():
            QMessageBox.warning(self, "Nom invalide", "Veuillez saisir un nom valide.")
            return

        if not ip:
            QMessageBox.warning(self, "Champ requis", "L'adresse IP ne peut pas être vide.")
            return

        if not self.ip.hasAcceptableInput():
            QMessageBox.warning(self, "Adresse IP invalide", "Veuillez saisir une adresse IP valide.")
            return

        print("Validé")
        if self.ip_conflict_checker is not None:
            existing_names = self.ip_conflict_checker(ip)
            if existing_names:
                names_text = ", ".join(f'"{name}"' for name in existing_names)
                msg = QMessageBox(self)
                msg.setWindowTitle("Attention")
                msg.setText(
                    f"Attention les PC {names_text} ont deja cette adresse IP attribuee.\nEtes vous sur de vouloir continuer ?"
                )
                btn_oui = msg.addButton("Oui", QMessageBox.ButtonRole.YesRole)
                btn_non = msg.addButton("Non", QMessageBox.ButtonRole.NoRole)
                msg.setDefaultButton(btn_non)
                msg.exec()
                if msg.clickedButton() == btn_non:
                    return

        pc = PC(nom, ip, self.mac.text())
        self.pc_created.emit(pc)
        print("Création du pc réussie")
        self.window().close()
