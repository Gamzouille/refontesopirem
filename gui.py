import sys
from fileinput import close

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


        # --- Barre de Menu ---
        menu = self.menuBar()

        #-- menu fichier --
        file_menu = menu.addMenu("&📁 Fichier")
        file_menu.addSeparator()
        file_submenu = file_menu.addMenu("Submenu")

        #--- menu périphérique ---
        periph_menu = menu.addMenu("&	🖧 Périphériques")


        #--- Menu other ---
        other_menu = menu.addMenu("⇪ Autres")



        #--- Boutons ---
        self.btn_pc = QAction("🖳 Ajouter un PC")
        self.btn_switch = QAction("🖴 Ajouter un switch")
        self.btn_quit = QAction("🗙 Quitter")


        print("OK 2")
        # --- Connexions boutons ---
        periph_menu.addAction(self.btn_pc)
        periph_menu.addAction(self.btn_switch)
        other_menu.addAction(self.btn_quit)

        # --- Triggers ---
        self.btn_pc.triggered.connect(self.ajoutePC)
        self.btn_quit.triggered.connect(self.close)

    print("OK 3")


    def ajoutePC(self):
        ordi = network.liste_pc[0]
        network.liste_pc.pop(0)


    #def supprimerPC(self):


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

