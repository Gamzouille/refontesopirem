import sys
from fileinput import close
from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QFrame, QGridLayout, \
    QLineEdit, QToolBar
import json
import network
from ui_nouveau_projet import ProjectWindow

with open("scenario.json") as f:
    data = json.load(f)

print("OK 1")

class HomeWindow(QMainWindow):
    def __init__(self, button_action2=None):
        super().__init__()
        self.setWindowTitle("Sopirem")
        self.setMinimumSize(800, 600)
        # --- Background ---


        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("White"))
        self.setPalette(palette)

        # --- Contenu principal ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QGridLayout()
        central.setLayout(layout)
        interface_layout = QGridLayout()
        central.setLayout(interface_layout)


        # --- Barre de Menu ---
        menu = self.menuBar()
        self.menuBar().setStyleSheet("""
            QMenuBar {
                background-color: rgb(49, 49, 49);
                color: rgb(255, 255, 255);
                border: 1px solid #000;
            }
            QMenuBar::item {
                background-color: rgb(49, 49, 49);
                color: rgb(255, 255, 255);
            }
            QMenuBar::item::selected {
                background-color: rgb(30, 30, 30);
            }
            QMenu {
                background-color: rgb(49, 49, 49);
                color: rgb(255, 255, 255);
                border: 1px solid #000;
            }
            QMenu::item::selected {
                background-color: rgb(30, 30, 30);
            }
        """)

        #-- menu fichier --
        file_menu = menu.addMenu("&📁 Fichier")
        file_menu.addSeparator()

        #--- menu périphérique ---
        periph_menu = menu.addMenu("&	🖧 Périphériques")


        #--- Menu option ---
        option_menu = menu.addMenu("⇪ Options")



        #--- Boutons ---
        self.btn_new = QAction("Nouveau projet")
        self.btn_open = QAction("Ouvrir")
        self.btn_save = QAction("Enregistrer")
        self.btn_resave = QAction("Enregistrer sous")

        self.btn_pc = QAction("🖳 Ajouter un PC")
        self.btn_switch = QAction("🖴 Ajouter un switch")
        self.btn_quit = QAction("🗙 Quitter")


        print("OK 2")
        # --- Connexions boutons ---
        file_menu.addAction(self.btn_new)
        file_menu.addAction(self.btn_open)
        file_menu.addAction(self.btn_save)
        file_menu.addAction(self.btn_resave)
        file_menu.addAction(self.btn_quit)

        periph_menu.addAction(self.btn_pc)
        periph_menu.addAction(self.btn_switch)


        # --- Triggers ---
        self.btn_new.triggered.connect(self.create_project)
        self.btn_pc.triggered.connect(self.ajoutePC)
        self.btn_quit.triggered.connect(self.close)

    print("OK 3")


    def ajoutePC(self):
        ordi = network.liste_pc[0]
        network.liste_pc.pop(0)
        btn_pc_icon = QPushButton()
        pixmap = QPixmap("image/pc_icon.png")
        icon = (QIcon(pixmap))
        btn_pc_icon.setIcon(icon)
        btn_pc_icon.setIconSize(pixmap.rect().size())
        layout.addWidget(btn_pc_icon)

    #def supprimerPC(self):

    def create_project(self):
        self.project_window = ProjectWindow()
        self.project_window.show()
        self.close()

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

