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

    def __new__(cls, nom, nb_ports=4):
        print("Création d'un nouvel objet Switch")
        instance = super(Switch, cls).__new__(cls)
        return instance

    def __init__(self, nom, nb_ports=4):
        self.nom = nom
        self.ports = {i: None for i in range(1, nb_ports + 1)}  # ports vides
        self.mac_table = {}  # Table MAC: mac -> port

    def connect(self, port_number, pc):
        self.ports[port_number] = pc
        pc.switch = self
        pc.switch_port = port_number

    def receive_trame(self, trame, incoming_port):
        print(f"[{self.nom}] Reçu {trame} sur le port {incoming_port}")

        #  Apprentissage : MAC source -> port
        self.mac_table[trame.source_mac] = incoming_port
        print(f"[{self.nom}] Appris {trame.source_mac} est sur le port {incoming_port}")

        #  Vérifier si la MAC de destination est connue
        dest_port = self.mac_table.get(trame.dest_mac)

        if dest_port and dest_port != incoming_port:
            # Unicast → envoi direct
            pc_dest = self.ports.get(dest_port)
            if pc_dest:
                print(f"[{self.nom}] Unicast {trame} vers port {dest_port} ({pc_dest.name})")
                pc_dest.receive_trame(trame)
        else:
            # Broadcast ou destination inconnue → flood
            for port, pc in self.ports.items():
                if pc and port != incoming_port:
                    print(f"[{self.nom}] Diffusion {trame} au port {port} ({pc.name})")
                    pc.receive_trame(trame)

    def show_mac_table(self):
        return f"Table MAC du switch {self.nom} : {self.mac_table}"

    def empty_mac_table(self):
        """Vide complètement la table MAC du switch."""
        self.mac_table.clear()
        print(f"[{self.nom}] Table MAC vidée.")
    def show(self):
        print(f"{self.nom}, {self.nb_ports}")



class PC:

    def __new__(cls, name, ip, mac):
        print("Création d'un nouvel objet PC")
        instance = super(PC, cls).__new__(cls)
        return instance


    def __init__(self, name, ip, mac):
        self.name = name
        self.ip = ip
        self.mac = mac
        self.arp_table = ARPTable()
        self.connected = []
        self.trames_envoyees = []
        self.switch = None
        self.switch_port = None

    def receive_trame(self, trame):
        print(f"[{self.name}] Reçu {trame}")

        if trame.type_trame == "ARP" and trame.dest_mac == "FF:FF:FF:FF:FF:FF":
            # Je suis la cible si mon IP correspond
            if trame.dest_ip == self.ip:
                reply = Trame(
                    source_ip=self.ip,
                    dest_ip=trame.source_ip,
                    source_mac=self.mac,
                    dest_mac=trame.source_mac,
                    type_trame="ARP-REPLY"
                )
                print(f"[{self.name}] Répond avec {reply}")
                self.switch.receive_trame(reply, self.switch_port)

        elif trame.type_trame == "ARP-REPLY" and trame.dest_ip == self.ip:
            # Mettre à jour mon cache ARP
            self.arp_table.add_entry(trame.source_ip, trame.source_mac)

        elif trame.type_trame == "ICMP" and trame.dest_ip == self.ip:
            print(f"[{self.name}] Ping reçu de {trame.source_ip} ({trame.source_mac}) → Réponse OK")

    def arp_request(self, target_ip):
        if self.switch:
            # Construire une trame ARP de diffusion (broadcast)
            trame = Trame(
                source_ip=self.ip,
                dest_ip=target_ip,
                source_mac=self.mac,
                dest_mac="FF:FF:FF:FF:FF:FF",  #  toujours broadcast
                type_trame="ARP"
            )
            self.trames_envoyees.append(trame)
            print(f"[{self.name}] Envoi {trame}")
            self.switch.receive_trame(trame, self.switch_port)
            return None, None  # La réponse arrivera plus tard (ARP-REPLY)
        return None, None

    def ping(self, target_ip):
        mac = self.arp_table.get_mac(target_ip)
        pc = None

        if not mac:
            # Envoie d'une requête ARP (diffusion)
            self.arp_request(target_ip)
            # Après diffusion, on regarde si une réponse a rempli le cache
            mac = self.arp_table.get_mac(target_ip)

        if mac:
            # Trouver le PC correspondant dans le switch
            pc = next((p for p in self.switch.ports.values()
                       if p and p.ip == target_ip), None)

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

    def empty_arp_table(self):
        """Vide complètement la table MAC du switch."""
        self.arp_table.table.clear()
        print(f"[{self.name}] Cache arp vidé.")

    def affiche_ip(self):
        return f"{self.ip}"

    def affiche_mac(self, mac):
        return f"{self.ip}"
    def show(self):
        print(f"{self.name}, {self.ip}, {self.mac}")

if __name__ == "__main__":
    import code


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
    print("pc1.affiche_ip()")
    print("  switch1.show_mac_table()  # pour voir la table mac du switch")
    print("  switch1.empty_mac_table()  # pour vider la table mac du switch")
    print("  pc1.empty_arp_table()  # pour vider le cache arp d'un pc")
    print("Tapez Ctrl+D (ou Ctrl+Z sur Windows) pour quitter\n")

    code.interact(local=locals())