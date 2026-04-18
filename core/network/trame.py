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