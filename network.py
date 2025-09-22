class ARPTable:
    def __init__(self):
        self.table = {}

    def add_entry(self, ip, mac):
        self.table[ip] = mac

    def get_mac(self, ip):
        return self.table.get(ip, None)

    def __repr__(self):
        return str(self.table)


class PC:
    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.arp_table = ARPTable()
        self.connected = []

    def connect(self, other_pc):
        self.connected.append(other_pc)
        other_pc.connected.append(self)

    def arp_request(self, target_ip):
        for pc in self.connected:
            if pc.ip == target_ip:
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
            return f"{self.name} → {pc.name} : Ping OK"
        else:
            return f"{self.name} : Impossible d’atteindre {target_ip}"

    def show_arp_cache(self):
        return f"Cache ARP {self.name} : {self.arp_table}"


if __name__ == "__main__":
    import code

    # Créer deux PCs et les connecter
    pc1 = PC("PC1", "192.168.1.1", "AA:BB:CC:DD:EE:01")
    pc2 = PC("PC2", "192.168.1.2", "AA:BB:CC:DD:EE:02")
    pc1.connect(pc2)

    print("=== Mini-terminal Sopirem ===")
    print("Vous pouvez maintenant taper des commandes Python comme :")
    print("  pc1.show_arp_cache()")
    print("  pc1.ping('192.168.1.2')")
    print("  pc2.show_arp_cache()")
    print("  pc2.ping('192.168.1.1')")
    print("Tapez Ctrl+D (ou Ctrl+Z sur Windows) pour quitter\n")

    # Ouvre un terminal interactif Python avec toutes les variables locales disponibles
    code.interact(local=locals())
