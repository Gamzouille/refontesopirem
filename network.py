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

class Switch:
    def __init__(self):
        self.ports = {}
        self.arp_table = ARPTable()

    def connect(self, port_number, pc):
        self.ports[port_number] = pc
        pc.switch = self  # chaque PC connaît son switch

    def receive_trame(self, trame, incoming_port):
        print(f"[Switch] Reçu {trame} sur le port {incoming_port}")
        self.arp_table.add_entry(trame.source_ip, trame.source_mac)

        dest_mac_known = False
        for port, pc in self.ports.items():
            if pc.mac == trame.dest_mac:
                dest_mac_known = True
                if port != incoming_port:  # ne renvoie pas au port source
                    print(f"[Switch] Transmet {trame} au port {port} ({pc.name})")
                    pc.receive_trame(trame)
        if not dest_mac_known:
            # diffusion à tous les ports sauf celui d'origine
            for port, pc in self.ports.items():
                if port != incoming_port:
                    print(f"[Switch] Diffusion {trame} au port {port} ({pc.name})")
                    pc.receive_trame(trame)

    def show_arp_cache(self):
        return f"Cache ARP Switch : {self.arp_table}"


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
                """Ajoute la trame dans la liste des trames envoyées"""
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
            """trame ICMP"""
            self.trames_envoyees.append(trame_ping)
            """L'ajoute dans la liste des trames envoyées"""
            print(f"[{self.name}] Envoi {trame_ping}")
            return f"{self.name} → {pc.name} : Ping OK"
        else:
            return f"{self.name} : Impossible d’atteindre {target_ip}"

    def show_arp_cache(self):
        return f"Cache ARP {self.name} : {self.arp_table}"

    def voir_trames(self):
        """méthode pour afficher les trames, pour le pc sur lequel la méthode..."""
        if not self.trames_envoyees:
            return f"{self.name} n'a envoyé aucune trame."
        for trame in self.trames_envoyees:
            print(trame)  # __repr__ sera appelé automatiquement ici


if __name__ == "__main__":
    import code

    # Créer deux PCs et les connecter
    pc1 = PC("PC1", "192.168.1.1", "AA:BB:CC:DD:EE:01")
    pc2 = PC("PC2", "192.168.1.2", "AA:BB:CC:DD:EE:02")
    pc1.connect(pc2)
    pc2.connect(pc1)

    print("=== Mini-terminal Sopirem ===")
    print("Vous pouvez maintenant taper des commandes Python comme :")
    print("  pc1.show_arp_cache()")
    print("  pc1.ping('192.168.1.2')")
    print("  pc1.voir_trames()")
    print("  pc2.show_arp_cache()")
    print("  pc2.ping('192.168.1.1')")
    print("  pc2.voir_trames()")
    print("trame = Trame(pc1.ip, pc2.ip, pc1.mac, pc2.mac, 'ARP'")
    print ("switch1.receive_trame(trame, incoming_port=1)")
    print("Tapez Ctrl+D (ou Ctrl+Z sur Windows) pour quitter\n")

    code.interact(local=locals())
