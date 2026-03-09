import os
import sys
from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon, QPen
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QListWidget, QComboBox, QGraphicsView, QGraphicsSceneMouseEvent, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QDialog, QVBoxLayout, QMessageBox
import json
import network
from form_pc import PcWindow
from form_switch import SwitchWindow

# Import fonctions
from fonctions.sauvegarde import sauvegarde_json

# Import classes
from classes.pc import PC
from classes.arptable import ARPTable
from classes.switch import Switch
from classes.trame import Trame


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
        self.devices = []  # liste de tous les QGraphicsPixmapItem ajoutés
        self.view = QGraphicsView(self.scene)
        layout.addWidget(self.view)
        self.scene.setBackgroundBrush(QColor("white"))
        self.view.setStyleSheet("background: white;")

        # --- devices gestion --- 
        self.devices = []  # liste de tous les QGraphicsPixmapItem ajoutés
        self.cables = []

        
        
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
        periph_menu = menu.addMenu("& Périphériques")

        # --- Menu options ---
        option_menu = menu.addMenu(" Options")

        # --- Actions ---
        self.btn_new = QAction("Nouveau projet")
        self.btn_open = QAction("Ouvrir")
        self.btn_save = QAction("Enregistrer")
        self.btn_resave = QAction("Enregistrer sous")

        self.btn_pc = QAction(" Ajouter un PC")
        self.btn_switch = QAction(" Ajouter un switch")
        self.btn_quit = QAction(" Quitter")
        self.btn_connect = QAction(" Connecter")
        
        # --- Ajout des actions ---
        file_menu.addAction(self.btn_new)
        file_menu.addAction(self.btn_open)
        file_menu.addAction(self.btn_save)
        file_menu.addAction(self.btn_resave)
        file_menu.addAction(self.btn_quit)
        periph_menu.addAction(self.btn_pc)
        periph_menu.addAction(self.btn_switch)
        periph_menu.addAction(self.btn_connect)

        # --- Connexions ---
        self.btn_new.triggered.connect(self.create_project)
        self.btn_pc.triggered.connect(self.ajoutePC)
        self.btn_switch.triggered.connect(self.ajouteSwitch)
        self.btn_quit.triggered.connect(self.close)
        self.btn_save.triggered.connect(self.save)
        self.btn_open.triggered.connect(self.open_file_dialog)
        self.btn_connect.triggered.connect(self.connecter)

        
        
    def sceneEventFilter(self, watched, event):
        if event.type() == event.GraphicsSceneMove:
            for c in self.cables:
                c.update_position()
        return False


    def save(self):
        fichier, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer",
            "",
            "Fichiers JSON (*.json)"
        )

        if not fichier:
            return

        data = {
            "PC": []
        }

        for i, item in enumerate(self.devices):
            if hasattr(item, "pc"):
                data["PC"].append(item.pc.to_dict())

        with open(fichier, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("✅ Projet sauvegardé")


            


    def ajoutePC(self):
        print("Je rentre bien ici")

        pixmap = QPixmap("images/pc_icon.png")

        item = MovablePixmapItem(pixmap)
        item.on_click = self.on_device_clicked
        self.scene.addItem(item)
        self.devices.append(item)
        item.setPos(50, 50)
        self.formPC(item)
        item.setScale(0.5)
        
        
        
        

    def ajouteSwitch(self):
        print("Je rentre bien ici")

        pixmap = QPixmap("images/switch_icon.png")

        item = MovablePixmapItem(pixmap)
        item.on_click = self.on_device_clicked
        self.scene.addItem(item)
        self.devices.append(item)
        item.setPos(100, 100)

        self.formSwitch()
        item.setScale(1.25)
        
        

    def formPC(self, item):
        self.formpc_window = PcWindow()
        self.formpc_window.pc_created.connect(
            lambda pc, current_item=item: self.attach_pc_to_item(current_item, pc)
        )
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

    def options_periph(self):
        self.option_window = OptionWindow()
        self.option_window.show()
        
        
    def connecter(self):
        if len(self.devices) < 2:
            return

        win = ConnectWindow(self.devices, self)
        if win.exec() == QDialog.DialogCode.Accepted:
            d1, d2 = win.get_selected_devices()
            if d1 is not d2:
                cable = Cable(d1, d2)
                self.scene.addItem(cable)
                self.cables.append(cable)

    def attach_pc_to_item(self, item, pc):
        item.pc = pc

    def on_device_clicked(self, item):
        if not hasattr(item, "pc"):
            return

        pc = item.pc
        QMessageBox.information(
            self,
            "Attributs du PC",
            f"Nom : {pc.name}\nIP : {pc.ip}\nAdresse MAC : {pc.mac}"
        )






class MovablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.cables = []
        self.on_click = None

    def itemChange(self, change, value):
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionChange:
            for cable in self.cables:
                cable.update_position()
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if callable(self.on_click):
            self.on_click(self)


class Cable(QGraphicsLineItem):
    def __init__(self, item1, item2):
        super().__init__()
        self.item1 = item1
        self.item2 = item2
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        self.setPen(pen)

        # Ajouter le câble aux périphériques
        self.item1.cables.append(self)
        self.item2.cables.append(self)

        self.update_position()

    def update_position(self):
        if self.scene() is None:
            return
        p1 = self.item1.sceneBoundingRect().center()
        p2 = self.item2.sceneBoundingRect().center()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())



class ConnectWindow(QDialog):
    def __init__(self, devices, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Connecter deux appareils")

        self.devices = devices
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Champs
        self.combo1 = QComboBox()
        self.combo2 = QComboBox()

        # Remplir avec "itemX"
        for i, d in enumerate(devices):
            self.combo1.addItem(f"Appareil {i+1}", d)
            self.combo2.addItem(f"Appareil {i+1}", d)

        layout.addWidget(QLabel("Périphérique 1 :"))
        layout.addWidget(self.combo1)
        layout.addWidget(QLabel("Périphérique 2 :"))
        layout.addWidget(self.combo2)

        # Bouton valider
        btn = QPushButton("Valider")
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)

    def get_selected_devices(self):
        d1 = self.combo1.currentData()
        d2 = self.combo2.currentData()
        return d1, d2


class OptionWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Options")
        self.setMinimumSize(300, 200)

print("OK 4")
def run_app():
    app = QApplication(sys.argv)
    window = HomeWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_app()
