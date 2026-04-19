from services.path_finding import find_path_between_items, reverse_path
from services.broadcast import build_broadcast_waves
from core.network.trame import Trame

from PyQt6.QtGui import QColor, QPalette, QAction, QPixmap, QIcon, QPen, QFont, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QGridLayout, QLabel, QFileDialog, QComboBox, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene, QGraphicsItem, QGraphicsLineItem, QDialog, QVBoxLayout, QMessageBox, QGraphicsSimpleTextItem, QMenu
from PyQt6.QtCore import Qt, QTimer, QLineF

def learn_switch_mac_along_path(self, source_mac, path):
        for cable, _from_item, to_item in path:
            if hasattr(to_item, "switch"):
                incoming_port = cable.get_port_for_item(to_item)
                if incoming_port is not None:
                    to_item.switch.mac_table[source_mac] = incoming_port

def build_ping_steps(self, source_item, destination_item, path):
        source_pc = source_item.pc
        destination_pc = destination_item.pc
        reverse_path_result = reverse_path(self, path)
        steps = []

        if source_pc.arp_table.get_mac(destination_pc.ip) != destination_pc.mac:
            broadcast_waves = build_broadcast_waves(self, source_item, destination_item)
            broadcast_path = [segment for wave in broadcast_waves for segment in wave]
            source_pc.trames_envoyees.append(
                Trame(
                    source_ip=source_pc.ip,
                    dest_ip=destination_pc.ip,
                    source_mac=source_pc.mac,
                    dest_mac="FF:FF:FF:FF:FF:FF",
                    type_trame="ARP",
                )
            )
            steps.extend(
                {
                    "segments": [
                        {
                            "cable": cable,
                            "from_item": from_item,
                            "to_item": to_item,
                        }
                        for cable, from_item, to_item in wave
                    ],
                    "color": QColor("#f39c12"),
                    "phase": "Requête ARP (broadcast)",
                }
                for wave in broadcast_waves
            )
            learn_switch_mac_along_path(self, source_pc.mac, broadcast_path)
            destination_pc.arp_table.add_entry(source_pc.ip, source_pc.mac)

            destination_pc.trames_envoyees.append(
                Trame(
                    source_ip=destination_pc.ip,
                    dest_ip=source_pc.ip,
                    source_mac=destination_pc.mac,
                    dest_mac=source_pc.mac,
                    type_trame="ARP-REPLY",
                )
            )
            steps.extend(
                {
                    "segments": [
                        {
                            "cable": cable,
                            "from_item": from_item,
                            "to_item": to_item,
                        }
                    ],
                    "color": QColor("#3498db"),
                    "phase": "Réponse ARP",
                }
                for cable, from_item, to_item in reverse_path_result
            )
            learn_switch_mac_along_path(self, destination_pc.mac, reverse_path_result)
            source_pc.arp_table.add_entry(destination_pc.ip, destination_pc.mac)

        source_pc.trames_envoyees.append(
            Trame(
                source_ip=source_pc.ip,
                dest_ip=destination_pc.ip,
                source_mac=source_pc.mac,
                dest_mac=destination_pc.mac,
                type_trame="ICMP",
            )
        )
        steps.extend(
            {
                "segments": [
                    {
                        "cable": cable,
                        "from_item": from_item,
                        "to_item": to_item,
                    }
                ],
                "color": QColor("#20b15a"),
                "phase": "Requête ICMP",
            }
            for cable, from_item, to_item in path
        )
        learn_switch_mac_along_path(self, source_pc.mac, path)

        destination_pc.trames_envoyees.append(
            Trame(
                source_ip=destination_pc.ip,
                dest_ip=source_pc.ip,
                source_mac=destination_pc.mac,
                dest_mac=source_pc.mac,
                type_trame="ICMP-REPLY",
            )
        )
        steps.extend(
            {
                "segments": [
                    {
                        "cable": cable,
                        "from_item": from_item,
                        "to_item": to_item,
                    }
                ],
                "color": QColor("#2ecc71"),
                "phase": "Réponse ICMP",
            }
            for cable, from_item, to_item in reverse_path_result
        )
        learn_switch_mac_along_path(self, destination_pc.mac, reverse_path_result)
        return steps

def launch_ping(self, source_item, destination_item):
        path = find_path_between_items(self, source_item, destination_item)
        if not path:
            QMessageBox.information(
                self,
                "Ping",
                f"Aucun chemin trouvé entre {source_item.pc.name} et {destination_item.pc.name}."
            )
            return

        ping_steps = build_ping_steps(self, source_item, destination_item, path)

        stop_ping_animation(self)
        self.current_ping_steps = ping_steps
        self.current_ping_step = 0
        self.current_ping_progress = 0.0
        self.current_ping_pause_ticks = 0

        if not self.current_ping_steps:
            return

        first_step = self.current_ping_steps[0]
        self.statusBar().showMessage(first_step["phase"])
        for segment in first_step["segments"]:
            segment["cable"].set_ping_direction(segment["from_item"], segment["to_item"])
            segment["cable"].set_ping_progress(0.0, first_step["color"])
        self.ping_animation_timer.start(25)

def stop_ping_animation(self):
        self.ping_animation_timer.stop()
        for cable in {
            segment["cable"]
            for step in self.current_ping_steps
            for segment in step["segments"]
        }:
            try:
                cable.stop_ping_animation()
            except RuntimeError:
                pass
        self.current_ping_steps = []
        self.current_ping_step = 0
        self.current_ping_progress = 0.0
        self.current_ping_pause_ticks = 0
        self.statusBar().clearMessage()


def advance_ping_animation(self):
        if not self.current_ping_steps:
            self.stop_ping_animation()
            return

        if self.current_ping_pause_ticks > 0:
            self.current_ping_pause_ticks -= 1
            return

        try:
            current_step = self.current_ping_steps[self.current_ping_step]
        except (IndexError, RuntimeError):
            self.stop_ping_animation()
            return
        self.current_ping_progress += 0.025
        try:
            for segment in current_step["segments"]:
                segment["cable"].set_ping_progress(self.current_ping_progress, current_step["color"])
        except RuntimeError:
            self.stop_ping_animation()
            return

        if self.current_ping_progress < 1.0:
            return

        try:
            for segment in current_step["segments"]:
                segment["cable"].set_ping_progress(1.0, current_step["color"])
        except RuntimeError:
            self.stop_ping_animation()
            return
        self.current_ping_step += 1
        self.current_ping_progress = 0.0

        if self.current_ping_step >= len(self.current_ping_steps):
            self.statusBar().showMessage("Ping terminé", 1200)
            QTimer.singleShot(250, self.stop_ping_animation)
            self.ping_animation_timer.stop()
            return

        try:
            next_step = self.current_ping_steps[self.current_ping_step]
            if next_step["phase"] != current_step["phase"]:
                self.statusBar().showMessage(next_step["phase"])
                self.current_ping_pause_ticks = 8
            for segment in next_step["segments"]:
                segment["cable"].set_ping_direction(segment["from_item"], segment["to_item"])
                segment["cable"].set_ping_progress(0.0, next_step["color"])
        except RuntimeError:
            self.stop_ping_animation()