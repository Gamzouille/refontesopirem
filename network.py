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
        self.trames_envoyees = []
        self.switch = None
        self.switch_port = None

    def arp_request(self, target_ip):
        if self.switch:
            # Envoi d'une trame ARP via le switch
            target_mac = self.switch.arp_table.get_mac(target_ip)
            trame = Trame(self.ip, target_ip, self.mac, target_mac or "FF:FF:FF:FF:FF:FF", type_trame="ARP")
            self.trames_envoyees.append(trame)
            print(f"[{self.name}] Envoi {trame}")
            self.switch.receive_trame(trame, self.switch_port)
            # Retourne le MAC si connu par le switch
            if target_mac:
                self.arp_table.add_entry(target_ip, target_mac)
                return target_mac, next((p for p in self.connected if isinstance(p, PC) and p.ip == target_ip), None)
        return None, None

    def ping(self, target_ip):
        mac = self.arp_table.get_mac(target_ip)
        if not mac:
            mac, pc = self.arp_request(target_ip)
        else:
            pc = next((p for p in self.connected if isinstance(p, PC) and p.ip == target_ip), None)

        if mac and pc:
            trame_ping = Trame(self.ip, pc.ip, self.mac, pc.mac, type_trame="ICMP")
            self.trames_envoyees.append(trame_ping)
            print(f"[{self.name}] Envoi {trame_ping}")
            if self.switch:
                self.switch.receive_trame(trame_ping, self.switch_port)
            return f"{self.name} → {pc.name} : Ping OK"
        else:
            return f"{self.name} : Impossible d'atteindre {target_ip}"

    def show_arp_cache(self):
        return f"Cache ARP {self.name} : {self.arp_table}"

    def voir_trames(self):
        if not self.trames_envoyees:
            print(f"{self.name} n'a envoyé aucune trame.")
        for trame in self.trames_envoyees:
            print(trame)


if __name__ == "__main__":
    import code
    # Créer deux PCs et les connecter directement
    pc1 = PC("PC1", "192.168.1.1", "AA:BB:CC:DD:EE:01")
    pc2 = PC("PC2", "192.168.1.2", "AA:BB:CC:DD:EE:02")

    # --- Exemple avec switch et ports ---
    switch1 = Switch("SW1", nb_ports=4)  # switch avec 4 ports
    switch1.connect(1, pc1)  # pc1 sur port 1
    switch1.connect(2, pc2)  # pc2 sur port 2

    print("=== Mini-terminal Sopirem ===")
    print("Vous pouvez maintenant taper des commandes Python comme :")
    print("  pc1.show_arp_cache()")
    print("  pc1.ping('192.168.1.2')")
    print("  pc1.voir_trames()")
    print("  pc2.show_arp_cache()")
    print("  pc2.ping('192.168.1.1')")
    print("  pc2.voir_trames()")
    print("  switch1.show_arp_cache()  # pour voir les ports et le cache ARP du switch")
    print("Tapez Ctrl+D (ou Ctrl+Z sur Windows) pour quitter\n")

    code.interact(local=locals())