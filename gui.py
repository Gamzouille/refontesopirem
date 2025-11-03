import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QLineEdit
import json
from ui_nouveau_projet import ProjectWindow
import network

with open("scenario.json") as f:
    data = json.load(f)

print("OK 1")

class HomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sopirem")
        self.setMinimumSize(800, 600)
        # --- Titre ---
        self.title = QLabel("Titre")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout1 = QVBoxLayout()
        layout1.addStretch(1)
        layout1.addWidget(self.title)

        # --- Boutons ---
        self.btn_pc = QPushButton("Ajouter un PC")
        self.btn_switch = QPushButton("Ajouter un switch")
        self.btn_quit = QPushButton("Quitter")
        for btn in (self.btn_pc, self.btn_switch, self.btn_quit):
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    border-radius: 12px;
                    background-color: #738eb0;
                    color: white;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #2e3947;
                }
            """)

        print("OK 2")
        # --- Connexions boutons ---
        self.btn_pc.clicked.connect(self.ajoutePC)
        self.btn_switch.clicked.connect(self.ajouteSwitch)
        self.btn_quit.clicked.connect(self.close)

        print("OK entrée Contenu Widget")
        # --- Contenu ---
        layout2 = QGridLayout()
        layout2.addWidget(self.btn_pc, 0, 0)
        layout2.addWidget(self.btn_switch, 0, 1)
        layout2.addWidget(self.btn_quit, 0, 2)

        print("OK Sortie Contenu Widget")


    print("OK 3")
    def ajoutePC(self):
        self.title.setText("Ajouter un PC(placeholder)")
        network.PC.name = QLabel("Entrez le nom du PC : ")
        nom = QLineEdit()
        network.PC.ip = QLabel("Entrez l'adresse IP du PC")
        ip = QLineEdit()

    def ajouteSwitch(self):
        self.title.setText("Ajouter un switch(placeholder)")
        network.Switch.name = input("Entrez le nom du Switch")
print("OK 4")
def run_app():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()

