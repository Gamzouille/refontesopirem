from classes.arptable import ARPTable
from classes.switch import Switch
from classes.trame import Trame

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