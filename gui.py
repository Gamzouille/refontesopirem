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
        interface_layout = QGridLayout()
        central.setLayout(interface_layout)

        # --- Widgets ---
        toolbar = QToolBar("Ma barre d'outil")
        self.addToolBar(toolbar)

        # --- Boutons ---
        # --- Boutons ---
        self.button_action = QAction("📁 Fichier", self)
        self.button_action.setStatusTip("This is your button")
        self.button_action.triggered.connect(self.toolbar_button_clicked)
        toolbar.addAction(self.button_action)
        self.btn_pc = QPushButton("🖧 Ajouter un PC")
        self.btn_switch = QPushButton("🖴 Ajouter un switch")
        self.btn_quit = QPushButton("🗙 Quitter")
        for btn in (self.btn_pc, self.btn_switch, self.btn_quit):
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                        QPushButton {
                            font-size: 16px;
                            border-radius: 0px;
                            background-color: #bdbdbd;
                            color: black;
                            padding: 5px;
                        }
                        QPushButton:hover {
                            background-color: #808080;
                        }
                    """)
        # vide


        print("OK 2")
        # --- Connexions boutons ---
        self.btn_pc.clicked.connect(self.ajoutePC)
        self.btn_switch.clicked.connect(self.ajouteSwitch)
        self.btn_quit.clicked.connect(self.close)

        # --- Contenu ---
        layout.addWidget(self.btn_pc, 0, 0)
        layout.addWidget(self.btn_switch, 0, 1)
        layout.addWidget(self.btn_quit, 0, 2)
        interface_layout.addWidget(toolbar, -1, 0)


    print("OK 3")

    def toolbar_button_clicked(self, s):
        print("click", s)

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

