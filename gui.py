import sys

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QLineEdit, QToolBar, QStatusBar, QCheckBox
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
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        # --- Boutons ---
        self.button_action = QAction(QIcon("bug.png"), "&Your button", self)
        self.button_action.setStatusTip("This is your button")
        self.button_action.triggered.connect(self.toolbar_button_clicked)
        self.button_action.setCheckable(True)
        toolbar.addAction(self.button_action)

        toolbar.addSeparator()

        button_action2 = QAction(QIcon("bug.png"), "Your &button2", self)
        button_action2.setStatusTip("This is your button2")
        button_action2.triggered.connect(self.toolbar_button_clicked)
        button_action2.setCheckable(True)
        toolbar.addAction(button_action2)

        self.setStatusBar(QStatusBar(self))

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        file_menu.addAction(self.button_action)
        file_menu.addSeparator()

        file_submenu = file_menu.addMenu("Submenu")
        file_submenu.addAction(button_action2)


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
        #vide


        print("OK 2")
        # --- Connexions boutons ---
        self.btn_pc.clicked.connect(self.ajoutePC)
        self.btn_switch.clicked.connect(self.ajouteSwitch)
        self.btn_quit.clicked.connect(self.close)

        # --- Contenu ---
        toolbar.addWidget(self.btn_pc)
        toolbar.addWidget(self.btn_switch)
        toolbar.addWidget(self.btn_quit)
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

