import sys

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QLineEdit, QToolBar
import json
import network

with open("scenario.json") as f:
    data = json.load(f)

print("OK 1")

class HomeWindow(QMainWindow):
    def __init__(self, button_action2=None):
        super().__init__()
        self.setWindowTitle("Sopirem")
        self.setMinimumSize(800, 600)
        # --- Titre ---

        # --- Contenu principal ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout()
        central.setLayout(layout)
        interface_layout = QGridLayout()
        central.setLayout(interface_layout)

        # --- Barre d'outils ---
        toolbar = QToolBar("Ma barre d'outil")
        self.addToolBar(toolbar)

        # --- Barre de Menu ---
        menu = self.menuBar()

        #-- menu fichier --
        file_menu = menu.addMenu("&📁 Fichier")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Submenu")

        #--- menu périphérique ---
        periph_menu = menu.addMenu("&	🖧 Périphériques")


        #--- Boutons ---
        self.btn_pc = QAction("🖳 Ajouter un PC")
        self.btn_switch = QAction("🖴 Ajouter un switch")
        self.btn_quit = QAction("🗙 Quitter")


        print("OK 2")
        # --- Connexions boutons ---
        periph_menu.addAction(self.btn_pc)
        periph_menu.addAction(self.btn_switch)


        # --- Triggers ---
        self.btn_pc.triggered.connect(self.ajoutePC)


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

