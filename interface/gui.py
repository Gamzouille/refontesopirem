import os
import sys
from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon, QPen, QFont, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QComboBox, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QDialog, QVBoxLayout, QMessageBox, QGraphicsSimpleTextItem, QMenu
from PyQt6.QtCore import Qt, QTimer, QLineF
import json

from interface.forms.form_pc import PcWindow
from services.connection import *
from services.ping import *
from core.devices.pc import PC

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


with open("data/scenario.json") as f:
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
        self.view = NetworkGraphicsView(self.scene, self)
        layout.addWidget(self.view)
        self.scene.setBackgroundBrush(QColor("white"))
        self.view.setStyleSheet("background: white;")

        # --- devices gestion --- 
        self.devices = []  # liste de tous les QGraphicsPixmapItem ajoutés
        self.cables = []
        self.connect_mode = False
        self.pending_connection_item = None
        self.temp_cable = None
        self.active_context_menu = None
        self.ping_animation_timer = QTimer(self)
        self.ping_animation_timer.timeout.connect(
    lambda: advance_ping_animation(self)
)
        self.current_ping_steps = []
        self.current_ping_step = 0
        self.current_ping_progress = 0.0
        self.current_ping_pause_ticks = 0

        
        
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
        self.btn_switch.triggered.connect(lambda: ajouteSwitch(self))
        self.btn_quit.triggered.connect(self.close)
        self.btn_save.triggered.connect(self.save)
        self.btn_open.triggered.connect(self.open_file_dialog)

        self.escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        self.escape_shortcut.activated.connect(self.cancel_connection_mode)

        
    def sceneEventFilter(self, watched, event):
        if event.type() == event.GraphicsSceneMove:
            for c in self.cables:
                c.update_position()
        return False

    def on_scene_mouse_move(self, scene_pos):
        if not self.connect_mode or self.pending_connection_item is None or self.temp_cable is None:
            return
        p1 = self.pending_connection_item.sceneBoundingRect().center()
        self.temp_cable.setLine(p1.x(), p1.y(), scene_pos.x(), scene_pos.y())


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

    def ajoutePC(self):
        print("Je rentre bien ici")
        pixmap = QPixmap("images/pc_icon.png")

        item = MovablePixmapItem(pixmap)
        item.device_type = "pc"
        item.set_device_name("PC")
        item.on_click = self.on_device_single_clicked
        item.on_double_click = self.on_device_clicked
        item.on_context_menu = self.show_empty_context_menu
        self.scene.addItem(item)
        self.devices.append(item)
        item.setPos(50, 50)
        #self.formPC(item)

        self.find_existing_pc_name_by_ip = lambda ip: [
            d.pc.name for d in self.devices if hasattr(d, "pc") and d.pc.ip == ip
        ]

        item.setScale(0.5)
        self._pc_window = PcWindow(self.find_existing_pc_name_by_ip)
        self._pc_window.pc_created.connect(
        lambda pc: self.attach_pc_to_item(item, pc)
        )
        self._pc_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self._pc_window.show()
        self._pc_window.raise_()
        self._pc_window.activateWindow()
        
        
    def connecter(self):
        self.connect_mode = True
        self.pending_connection_item = None
        if self.temp_cable is not None and self.temp_cable.scene() is not None:
            self.scene.removeItem(self.temp_cable)
        self.temp_cable = None
        self.view.setFocus()

    def connecter_depuis_item(self, item):
        self.connecter()
        self.pending_connection_item = item
        self.temp_cable = QGraphicsLineItem()
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        self.temp_cable.setPen(pen)
        p1 = item.sceneBoundingRect().center()
        self.temp_cable.setLine(p1.x(), p1.y(), p1.x(), p1.y())
        self.scene.addItem(self.temp_cable)

    def cancel_connection_mode(self):
        self.connect_mode = False
        self.pending_connection_item = None
        if self.temp_cable is not None and self.temp_cable.scene() is not None:
            self.scene.removeItem(self.temp_cable)
        self.temp_cable = None

    def attach_pc_to_item(self, item, pc):
        item.pc = pc
        item.set_device_name(pc.name)
        item.set_device_subtitle(pc.ip)

    def attach_switch_to_item(self, item, sw):
        item.switch = sw
        item.set_device_name(sw.nom)
        item.set_device_subtitle("")

    def remove_device_item(self, item):
        if self.pending_connection_item is item:
            self.cancel_connection_mode()
        self.disconnect_machine(item)
        if item in self.devices:
            self.devices.remove(item)
        if item.scene() is not None:
            self.scene.removeItem(item)

    def on_device_clicked(self, item):
        if hasattr(item, "pc"):
            pc = item.pc
            QMessageBox.information(
                self,
                "Attributs du PC",
                f"Nom : {pc.name}\nIP : {pc.ip}\nAdresse MAC : {pc.mac}\n\nConnexions:\n{self.build_connections_text(item)}"
            )
            return

        if hasattr(item, "switch"):
            sw = item.switch
            QMessageBox.information(
                self,
                "Attributs du switch",
                f"Nom : {sw.nom}\nNombre de ports : {len(sw.ports)}\n\nConnexions:\n{self.build_connections_text(item)}"
            )
            return


    def show_empty_context_menu(self, item, screen_pos):
        self.scene.clearSelection()
        item.setSelected(True)

        menu = QMenu(self)
        cable_details = self.get_cable_details_for_item(item)

        info_action = menu.addAction("Voir les infos")
        info_action.triggered.connect(lambda: self.on_device_clicked(item))

        cache_label = "Voir le cache ARP" if hasattr(item, "pc") else "Voir la table MAC"
        cache_action = menu.addAction(cache_label)
        cache_action.triggered.connect(lambda: self.show_cache_for_item(item))

        menu.addSeparator()
        connect_action = menu.addAction("Connecter")
        connect_action.triggered.connect(lambda: self.connecter_depuis_item(item))

        if hasattr(item, "pc"):
            ping_menu = menu.addMenu("Ping")
            pc_targets = [
                device for device in self.devices
                if device is not item and hasattr(device, "pc")
            ]
            if not pc_targets:
                no_ping_target = ping_menu.addAction("Aucun PC disponible")
                no_ping_target.setEnabled(False)
                ping_menu.setEnabled(False)
            else:
                pc_targets.sort(key=lambda device: device.pc.name.lower())
                for target in pc_targets:
                    action = ping_menu.addAction(target.pc.name)
                    action.triggered.connect(
                        lambda checked=False, source=item, destination=target: self.launch_ping(source, destination)
                    )

        disconnect_menu = menu.addMenu("Déconnecter")

        if not cable_details:
            no_action = disconnect_menu.addAction("Aucune connexion à déconnecter")
            no_action.setEnabled(False)
            disconnect_menu.setEnabled(False)
        else:
            if hasattr(item, "switch"):
                cable_details.sort(
                    key=lambda d: (
                        d["own_port"] is None,
                        d["own_port"] if d["own_port"] is not None else 10**9,
                    )
                )
            else:
                cable_details.sort(key=lambda d: self.get_device_name(d["other"]).lower())

            for detail in cable_details:
                other = detail["other"]
                own_port = detail["own_port"]
                other_port = detail["other_port"]
                other_type = "PC" if hasattr(other, "pc") else "Switch" if hasattr(other, "switch") else "Appareil"
                other_name = self.get_device_name(other)
                label = f"{other_type} {other_name}"
                if hasattr(item, "switch") and own_port is not None:
                    label += f" (port local {own_port})"
                if hasattr(other, "switch") and other_port is not None:
                    label += f" (port distant {other_port})"
                action = disconnect_menu.addAction(label)
                action.triggered.connect(lambda checked=False, c=detail["cable"]: self.disconnect_cable(c))

        menu.addSeparator()
        delete_action = menu.addAction("Supprimer")
        delete_action.triggered.connect(lambda: self.remove_device_item(item))

        self.active_context_menu = menu
        menu.aboutToHide.connect(lambda: setattr(self, "active_context_menu", None))
        menu.popup(screen_pos)

    def is_connectable_device(self, item):
        return hasattr(item, "pc") or hasattr(item, "switch")

    def get_device_name(self, item):
        if hasattr(item, "pc"):
            return item.pc.name
        if hasattr(item, "switch"):
            return item.switch.nom
        return "Appareil"


    def format_pc_arp_cache(self, pc):
        entries = []
        if hasattr(pc.arp_table, "items"):
            entries = list(pc.arp_table.items())
        elif hasattr(pc.arp_table, "table"):
            entries = list(pc.arp_table.table.items())

        if not entries:
            return "Cache ARP vide"

        return "\n".join(f"- {ip} -> {mac}" for ip, mac in sorted(entries))

    def format_switch_mac_table(self, sw):
        lines = []
        for mac, port in sorted(sw.mac_table.items(), key=lambda item: str(item[0]).lower()):
            lines.append(f"- {mac} -> port {port}")

        uplinks = sorted(getattr(sw, "uplink_ports", set()))
        for port in uplinks:
            lines.append(f"- uplink -> port {port}")

        if not lines:
            return "Table MAC vide"
        return "\n".join(lines)

    def show_cache_for_item(self, item):
        if hasattr(item, "pc"):
            QMessageBox.information(
                self,
                f"Cache ARP de {item.pc.name}",
                self.format_pc_arp_cache(item.pc)
            )
            return

        if hasattr(item, "switch"):
            QMessageBox.information(
                self,
                f"Table MAC de {item.switch.nom}",
                self.format_switch_mac_table(item.switch)
            )
            return


    def on_device_single_clicked(self, item):
        if not self.connect_mode:
            return False
        if not self.is_connectable_device(item):
            return True

        if self.pending_connection_item is None:
            self.pending_connection_item = item
            self.temp_cable = QGraphicsLineItem()
            pen = QPen(QColor("black"))
            pen.setWidth(2)
            self.temp_cable.setPen(pen)
            p1 = item.sceneBoundingRect().center()
            self.temp_cable.setLine(p1.x(), p1.y(), p1.x(), p1.y())
            self.scene.addItem(self.temp_cable)
            return True

        if item is self.pending_connection_item:
            return True

        first = self.pending_connection_item
        for cable in self.cables:
            if (cable.item1 is first and cable.item2 is item) or (cable.item2 is first and cable.item1 is item):
                QMessageBox.information(self, "Connexion existante", "Ces deux machines sont deja connectées.")
                return True

        connection_config = {}
        if hasattr(first, "switch") or hasattr(item, "switch"):
            config_dialog = LinkConfigWindow(first, item, self)
            if config_dialog.exec() != QDialog.DialogCode.Accepted:
                return True
            connection_config = config_dialog.get_config()
            if not self.apply_connection_config(first, item, connection_config):
                return True

        cable = Cable(self.pending_connection_item, item)
        cable.connection_config = connection_config
        self.scene.addItem(cable)
        cable.update_position()
        self.cables.append(cable)
        self.cancel_connection_mode()
        return True






class MovablePixmapItem(QGraphicsPixmapItem):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable |
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable |
            QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.cables = []
        self.on_click = None
        self.on_double_click = None
        self.on_context_menu = None
        self.name_item = None
        self.subtitle_item = None

    def set_device_name(self, name):
        if self.name_item is None:
            self.name_item = QGraphicsSimpleTextItem(self)
        self.name_item.setText(name)
        self.update_name_style()
        self.update_name_position()

    def set_device_subtitle(self, subtitle):
        if self.subtitle_item is None:
            self.subtitle_item = QGraphicsSimpleTextItem(self)
        self.subtitle_item.setText(subtitle)
        self.update_name_style()
        self.update_name_position()

    def update_name_style(self):
        if self.name_item is None:
            return
        try:
            font = QFont("Arial")
            font.setPointSize(15)
            font.setBold(False)
            self.name_item.setFont(font)
            self.name_item.setBrush(QColor("black"))
            current_scale = self.scale() if self.scale() != 0 else 1.0
            self.name_item.setScale(1.0 / current_scale)
            if self.subtitle_item is not None:
                subtitle_font = QFont("Arial")
                subtitle_font.setPointSize(11)
                subtitle_font.setBold(False)
                self.subtitle_item.setFont(subtitle_font)
                self.subtitle_item.setBrush(QColor("black"))
                self.subtitle_item.setScale(1.0 / current_scale)
        except RuntimeError:
            return

    def update_name_position(self):
        if self.name_item is None:
            return
        try:
            rect = self.boundingRect()
            current_scale = self.scale() if self.scale() != 0 else 1.0
            name_rect = self.name_item.boundingRect()
            effective_name_width = name_rect.width() / current_scale
            x = (rect.width() - effective_name_width) / 2
            y = rect.height() + 4
            self.name_item.setPos(x, y)
            subtitle_text = ""
            if self.subtitle_item is not None:
                try:
                    subtitle_text = self.subtitle_item.text()
                except RuntimeError:
                    subtitle_text = ""
            if self.subtitle_item is not None and subtitle_text:
                subtitle_rect = self.subtitle_item.boundingRect()
                effective_subtitle_width = subtitle_rect.width() / current_scale
                subtitle_x = (rect.width() - effective_subtitle_width) / 2
                subtitle_y = y + (name_rect.height() / current_scale) + 2
                self.subtitle_item.setPos(subtitle_x, subtitle_y)
        except RuntimeError:
            return

    def itemChange(self, change, value):
        if change in (
            QGraphicsItem.GraphicsItemChange.ItemPositionChange,
            QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged,
        ):
            for cable in self.cables:
                cable.update_position()
        return super().itemChange(change, value)

    def setScale(self, scale):
        super().setScale(scale)
        self.update_name_style()
        self.update_name_position()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if callable(self.on_double_click):
            self.on_double_click(self)

    def mousePressEvent(self, event):
        if callable(self.on_click) and self.on_click(self):
            event.accept()
            return
        super().mousePressEvent(event)

    def contextMenuEvent(self, event):
        if callable(self.on_context_menu):
            self.on_context_menu(self, event.screenPos())
            event.accept()
            return
        super().contextMenuEvent(event)


class NetworkGraphicsView(QGraphicsView):
    def __init__(self, scene, parent_window):
        super().__init__(scene)
        self.parent_window = parent_window
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        scene_pos = self.mapToScene(event.pos())
        self.parent_window.on_scene_mouse_move(scene_pos)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape and self.parent_window.connect_mode:
            self.parent_window.cancel_connection_mode()
            event.accept()
            return
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.MouseButton.RightButton
            and self.parent_window.connect_mode
            and self.parent_window.pending_connection_item is not None
        ):
            self.parent_window.cancel_connection_mode()
            event.accept()
            return
        super().mousePressEvent(event)


class Cable(QGraphicsLineItem):
    def __init__(self, item1, item2):
        super().__init__()
        self.item1 = item1
        self.item2 = item2
        self.connection_config = {}
        self.ping_progress = None
        self.ping_start_item = None
        self.ping_end_item = None
        self.ping_color = QColor("#20b15a")
        pen = QPen(QColor("black"))
        pen.setWidth(2)
        self.setPen(pen)

        # Ajouter le câble aux périphériques
        self.item1.cables.append(self)
        self.item2.cables.append(self)

        self.update_position()

    def update_position(self):
        try:
            if self.scene() is None:
                return
            p1 = self.item1.sceneBoundingRect().center()
            p2 = self.item2.sceneBoundingRect().center()
            self.setLine(p1.x(), p1.y(), p2.x(), p2.y())
        except RuntimeError:
            return

    def get_port_for_item(self, item):
        if item is self.item1:
            return self.connection_config.get("switch1_port")
        if item is self.item2:
            return self.connection_config.get("switch2_port")
        return None

    def set_ping_direction(self, start_item, end_item):
        self.ping_start_item = start_item
        self.ping_end_item = end_item

    def set_ping_progress(self, progress, color=None):
        self.ping_progress = progress
        if color is not None:
            self.ping_color = color
        self.update()

    def stop_ping_animation(self):
        self.ping_progress = None
        self.ping_start_item = None
        self.ping_end_item = None
        self.ping_color = QColor("#20b15a")
        self.update()

    def paint(self, painter, option, widget=None):
        try:
            super().paint(painter, option, widget)
            if self.ping_progress is None or self.ping_start_item is None or self.ping_end_item is None:
                return

            if self.ping_start_item is self.item1 and self.ping_end_item is self.item2:
                start_point = self.line().p1()
                end_point = self.line().p2()
            else:
                start_point = self.line().p2()
                end_point = self.line().p1()

            line = QLineF(start_point, end_point)
            if line.length() == 0:
                return

            segment_length = min(28.0, line.length() * 0.35)
            start_ratio = max(0.0, self.ping_progress - (segment_length / line.length()))
            animated_start = line.pointAt(start_ratio)
            animated_end = line.pointAt(min(self.ping_progress, 1.0))

            ping_pen = QPen(self.ping_color)
            ping_pen.setWidth(6)
            ping_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(ping_pen)
            painter.drawLine(animated_start, animated_end)
        except RuntimeError:
            return



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


class LinkConfigWindow(QDialog):
    def __init__(self, item1, item2, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configurer la connexion")
        self.item1 = item1
        self.item2 = item2

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.switch1_combo = None
        self.switch2_combo = None

        layout.addWidget(QLabel(f"Connexion : {self._name(item1)} ↔ {self._name(item2)}"))

        if hasattr(item1, "switch"):
            layout.addWidget(QLabel(f"Port de {item1.switch.nom} :"))
            self.switch1_combo = QComboBox()
            self._fill_switch_ports(self.switch1_combo, item1.switch)
            layout.addWidget(self.switch1_combo)

        if hasattr(item2, "switch"):
            layout.addWidget(QLabel(f"Port de {item2.switch.nom} :"))
            self.switch2_combo = QComboBox()
            self._fill_switch_ports(self.switch2_combo, item2.switch)
            layout.addWidget(self.switch2_combo)

        self.btn_validate = QPushButton("Valider")
        btn_cancel = QPushButton("Annuler")
        self.btn_validate.clicked.connect(self.accept)
        btn_cancel.clicked.connect(self.reject)
        layout.addWidget(self.btn_validate)
        layout.addWidget(btn_cancel)
        self._update_validate_state()

    def _name(self, item):
        if hasattr(item, "pc"):
            return item.pc.name
        if hasattr(item, "switch"):
            return item.switch.nom
        return "Appareil"

    def get_config(self):
        config = {}
        if self.switch1_combo is not None:
            config["switch1_port"] = self.switch1_combo.currentData()
        if self.switch2_combo is not None:
            config["switch2_port"] = self.switch2_combo.currentData()
        return config

    def _fill_switch_ports(self, combo, sw):
        used_ports = {port for port, value in sw.ports.items() if value is not None}
        used_ports.update(getattr(sw, "uplink_ports", set()))
        for p in sorted(sw.ports.keys()):
            is_used = p in used_ports
            label = f"{p} (utilise)" if is_used else str(p)
            combo.addItem(label, p)
            idx = combo.count() - 1
            model_item = combo.model().item(idx)
            if is_used and model_item is not None:
                model_item.setEnabled(False)

        for idx in range(combo.count()):
            model_item = combo.model().item(idx)
            if model_item is None or model_item.isEnabled():
                combo.setCurrentIndex(idx)
                break

    def _combo_has_enabled_item(self, combo):
        if combo is None:
            return True
        for idx in range(combo.count()):
            model_item = combo.model().item(idx)
            if model_item is None or model_item.isEnabled():
                return True
        return False

    def _update_validate_state(self):
        can_validate = self._combo_has_enabled_item(self.switch1_combo) and self._combo_has_enabled_item(self.switch2_combo)
        self.btn_validate.setEnabled(can_validate)


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
