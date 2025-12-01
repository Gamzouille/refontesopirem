import os
import sys
from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QListWidget, QComboBox, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem
import json
import network
from ui_nouveau_projet import ProjectWindow
from form_pc import PcWindow
from form_switch import SwitchWindow
from fonctions.sauvegarde import sauvegarde_json

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

        # --- Zone graphique déplaçable ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        self.scene.setBackgroundBrush(QColor("white"))
        self.view.setStyleSheet("background: white;")


        # --- Barre de Menu ---
        menu = self.menuBar()
        self.menuBar().setStyleSheet("""
        QMenuBar {
            background-color: white;
            color: black;
            border: 1px solid #ddd;
        }
        QMenuBar::item {
            background-color: white;
            color: black;
        }
        QMenuBar::item:selected {
            background-color: #f0f0f0;
            color: black;
        }
        QMenu {
            background-color: white;
            color: black;
            border: 1px solid #ddd;
        }
        QMenu::item:selected {
            background-color: #f0f0f0;
            color: black;
        }
""")

        # -- menu fichier --
        file_menu = menu.addMenu("&📁 Fichier")
        file_menu.addSeparator()

        # --- menu périphérique ---
        periph_menu = menu.addMenu("&🖧 Périphériques")

        # --- Menu options ---
        option_menu = menu.addMenu("⇪ Options")

        # --- Actions ---
        self.btn_new = QAction("Nouveau projet")
        self.btn_open = QAction("Ouvrir")
        self.btn_save = QAction("Enregistrer")
        self.btn_resave = QAction("Enregistrer sous")

        self.btn_pc = QAction("🖳 Ajouter un PC")
        self.btn_switch = QAction("🖴 Ajouter un switch")
        self.btn_quit = QAction("🗙 Quitter")

        # --- Ajout des actions ---
        file_menu.addAction(self.btn_new)
        file_menu.addAction(self.btn_open)
        file_menu.addAction(self.btn_save)
        file_menu.addAction(self.btn_resave)
        file_menu.addAction(self.btn_quit)

        periph_menu.addAction(self.btn_pc)
        periph_menu.addAction(self.btn_switch)

        # --- Connexions ---
        self.btn_new.triggered.connect(self.create_project)
        self.btn_pc.triggered.connect(self.ajoutePC)
        self.btn_switch.triggered.connect(self.ajouteSwitch)
        self.btn_quit.triggered.connect(self.close)
        self.btn_save.triggered.connect(self.save)
        self.btn_open.triggered.connect(self.open_file_dialog)

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

        pixmap = QPixmap("images/pc_icon.png")

        item = MovablePixmapItem(pixmap)
        self.scene.addItem(item)
        item.setPos(50, 50)
        self.formPC()
        item.setScale(0.5)
        
        
        

    def ajouteSwitch(self):
        print("Je rentre bien ici")

        pixmap = QPixmap("images/switch_icon.png")

        item = MovablePixmapItem(pixmap)
        self.scene.addItem(item)

        item.setPos(100, 100)

        self.formSwitch()
        item.setScale(1.25)

    def formPC(self):
        self.formpc_window = PcWindow()
        self.formpc_window.show()

    def formSwitch(self):
        self.forms_window = SwitchWindow()
        self.forms_window.show()

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

class MovablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        )


print("OK 4")
def run_app():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()

