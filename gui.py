import os
import sys
from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, \
    QListWidget, QComboBox
import json
import network
from ui_nouveau_projet import ProjectWindow
from form_pc import PcWindow

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

        print("J'instancie le menu")

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
        self.btn_switch.triggered.connect(self.ajouteSwitch)
        self.btn_quit.triggered.connect(self.close)
        self.btn_save.triggered.connect(self.save)
        self.btn_open.triggered.connect(self.open_file_dialog)
    print("OK 3")

    def save(self):
        fichier, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer un fichier",
            "",
            "Fichiers JSON (*.json)"
        )
        if fichier:
            # Ici, vous pouvez écrire les données dans le fichier sélectionné
            with open(fichier, 'w', encoding='utf-8') as f:
                f.write("Contenu à enregistrer\n")
            print(f"Fichier enregistré sous : {fichier}")


    def ajoutePC(self):
        print("Je rentre bien ici")

        label = QLabel(self)
        pixmap = QPixmap("images/pc_icon.png")
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())
        self.formPC()

    def formPC(self):
        self.form_window = PcWindow()
        self.form_window.show()

        #def supprimerPC(self):

    def open_file_dialog(self):
        file_filter = 'Data File (*.json)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption="Open file",
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter,
        )
        if response[0]:
            with open(response[0], 'r', encoding='utf-8') as f:
                data = json.load(f)

    def create_project(self):
        self.project_window = ProjectWindow()
        self.project_window.show()
        self.close()

    def ajouteSwitch(self):
        print("Je rentre bien ici")

        label = QLabel(self)
        pixmap = QPixmap("images/switch_icon.png")
        label.setPixmap(pixmap)
        self.setCentralWidget(label)
        self.resize(pixmap.width(), pixmap.height())

print("OK 4")
def run_app():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()

