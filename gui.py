import sys
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout
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

        # --- Contenu principal ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout()
        central.setLayout(layout)

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


        # --- Contenu ---
        layout = QGridLayout()
        layout.addWidget(self.btn_pc, 0, 0)
        layout.addWidget(self.btn_switch, 0, 1)
        layout.addWidget(self.btn_quit, 0, 2)

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

