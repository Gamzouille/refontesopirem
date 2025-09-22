from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel,
    QTextEdit, QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsLineItem
)
from PyQt6.QtGui import QPen, QColor
from PyQt6.QtCore import Qt
import sys


class ARPTable:
    def __init__(self):
        self.table = {}

    def add_entry(self, ip, mac):
        self.table[ip] = mac

    def get_mac(self, ip):
        return self.table.get(ip, None)

    def __repr__(self):
        return str(self.table)


class Trame:
    def __init__(self, source_ip, dest_ip, source_mac, dest_mac, type_trame="ARP"):
        self.source_ip = source_ip
        self.dest_ip = dest_ip
        self.source_mac = source_mac
        self.dest_mac = dest_mac
        self.type_trame = type_trame

    def __repr__(self):
        """Permet d'afficher les trames automatiquement lors d'un ping"""
        return (f"Trame(type={self.type_trame}, "
                f"{self.source_ip}({self.source_mac}) → {self.dest_ip}({self.dest_mac}))")


class PC:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.arp_table = ARPTable()
        self.connected = []
        self.trames_envoyees = []  # Historique des trames envoyées

    def connect(self, other_pc):
        self.connected.append(other_pc)
        other_pc.connected.append(self)

    def arp_request(self, target_ip):
        for pc in self.connected:
            if pc.ip == target_ip:
                trame = Trame(self.ip, pc.ip, self.mac, pc.mac, type_trame="ARP")
                self.trames_envoyees.append(trame)
                print(f"[{self.name}] Envoi {trame}")
                return pc.mac, pc
        return None, None

    def ping(self, target_ip):
        mac = self.arp_table.get_mac(target_ip)
        if not mac:
            mac, pc = self.arp_request(target_ip)
            if mac:
                self.arp_table.add_entry(pc.ip, pc.mac)
        else:
            pc = next((p for p in self.connected if p.ip == target_ip), None)

        if mac and pc:
            trame_ping = Trame(self.ip, pc.ip, self.mac, pc.mac, type_trame="ICMP")
            self.trames_envoyees.append(trame_ping)
            print(f"[{self.name}] Envoi {trame_ping}")
            return f"{self.name} → {pc.name} : Ping OK"
        else:
            return f"{self.name} : Impossible d’atteindre {target_ip}"

    def show_arp_cache(self):
        return f"Cache ARP {self.name} : {self.arp_table}"

    def voir_trames(self):
        if not self.trames_envoyees:
            return f"{self.name} n'a envoyé aucune trame."
        return "\n".join(str(trame) for trame in self.trames_envoyees)


# === Interface graphique ===
class NetworkSimulator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sopirem - Simulateur Réseau")
        self.setGeometry(100, 100, 800, 600)

        # === Zone graphique ===
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(50, 50, 400, 300)

        # PC1
        self.pc1_node = QGraphicsEllipseItem(0, 0, 50, 50)
        self.pc1_node.setBrush(QColor("red"))
        self.scene.addItem(self.pc1_node)
        self.pc1_node.setPos(50, 100)

        # PC2
        self.pc2_node = QGraphicsEllipseItem(0, 0, 50, 50)
        self.pc2_node.setBrush(QColor("blue"))
        self.scene.addItem(self.pc2_node)
        self.pc2_node.setPos(300, 100)

        # Lien
        line = QGraphicsLineItem(75, 125, 325, 125)
        line.setPen(QPen(Qt.GlobalColor.black, 2))
        self.scene.addItem(line)

        # Labels
        self.label_pc1 = QLabel("PC1", self)
        self.label_pc1.move(80, 180)
        self.label_pc2 = QLabel("PC2", self)
        self.label_pc2.move(330, 180)

        # Zone de logs
        self.logs = QTextEdit(self)
        self.logs.setGeometry(500, 50, 250, 300)
        self.logs.setReadOnly(True)

        # Boutons
        self.btn_ping1 = QPushButton("Ping PC2 depuis PC1", self)
        self.btn_ping1.setGeometry(50, 400, 200, 40)
        self.btn_ping1.clicked.connect(self.ping_from_pc1)

        self.btn_ping2 = QPushButton("Ping PC1 depuis PC2", self)
        self.btn_ping2.setGeometry(300, 400, 200, 40)
        self.btn_ping2.clicked.connect(self.ping_from_pc2)

        self.btn_cache1 = QPushButton("Cache ARP PC1", self)
        self.btn_cache1.setGeometry(50, 460, 200, 40)
        self.btn_cache1.clicked.connect(self.show_cache_pc1)

        self.btn_cache2 = QPushButton("Cache ARP PC2", self)
        self.btn_cache2.setGeometry(300, 460, 200, 40)
        self.btn_cache2.clicked.connect(self.show_cache_pc2)

        # === Logique réseau ===
        self.pc1 = PC("PC1", "192.168.1.1", "AA:BB:CC:DD:EE:01")
        self.pc2 = PC("PC2", "192.168.1.2", "AA:BB:CC:DD:EE:02")
        self.pc1.connect(self.pc2)

    def ping_from_pc1(self):
        result = self.pc1.ping(self.pc2.ip)
        self.logs.append(result)

    def ping_from_pc2(self):
        result = self.pc2.ping(self.pc1.ip)
        self.logs.append(result)

    def show_cache_pc1(self):
        self.logs.append(self.pc1.show_arp_cache())

    def show_cache_pc2(self):
        self.logs.append(self.pc2.show_arp_cache())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkSimulator()
    window.show()
    sys.exit(app.exec())
