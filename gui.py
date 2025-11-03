import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout
import json
from ui_nouveau_projet import ProjectWindow
import network

with open("scenario.json") as f:
    data = json.load(f)



class Fenetre(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sopirem")

        # --- Titre ---

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


        # --- Connexions boutons ---
        self.btn_pc.clicked.connect(self.ajoutePC)
        self.btn_switch.clicked.connect(self.ajouteSwitch)
        self.btn_quit.clicked.connect(self.close)


        # --- Contenu ---
        layout = QGridLayout()
        layout.addWidget(self.btn_pc, 0, 0)
        layout.addWidget(self.btn_switch, 0, 1)
        layout.addWidget(self.btn_quit, 0, 2)

    def ajoutePC(self):
        self.title.setText("Ajouter un PC(placeholder)")
        network.PC.name = input("Entrez le nom du PC : ")
        network.PC.ip = input("Entrez l'adresse IP du PC")

    def ajouteSwitch(self):
        self.title.setText("Ajouter un switch(placeholder)")
        network.Switch.name = input("Entrez le nom du Switch")

def run_app():
    app = QApplication(sys.argv)
    window = Fenetre()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()