class Switch:
    def __init__(self, nom, nb_ports=4):
        self.nom = nom
        self.ports = {i: None for i in range(1, nb_ports + 1)}  # ports vides
        self.mac_table = {}  # Table MAC: mac -> port

    def to_dict(self):
        return {
        "nom": self.nom,
        "nb_ports": len(self.ports)
    }

    @classmethod
    def from_dict(cls, data):
        return cls(
        nom=data["nom"],
        nb_ports=data["nb_ports"]
    )

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

    
    def formSwitch(self, item):
        self.forms_window = SwitchWindow()
        self.forms_window.switch_created.connect(
            lambda sw, current_item=item: self.attach_switch_to_item(current_item, sw)
        )
        self.forms_window.cancelled.connect(
            lambda current_item=item: self.remove_device_item(current_item)
        )
        self.forms_window.show()