from services.path_finding import find_path_between_items, reverse_path
from services.broadcast import build_broadcast_waves

def learn_switch_mac_along_path(self, source_mac, path):
        for cable, _from_item, to_item in path:
            if hasattr(to_item, "switch"):
                incoming_port = cable.get_port_for_item(to_item)
                if incoming_port is not None:
                    to_item.switch.mac_table[source_mac] = incoming_port

def build_ping_steps(self, source_item, destination_item, path):
        source_pc = source_item.pc
        destination_pc = destination_item.pc
        reverse_path = self.reverse_path(path)
        steps = []

        if source_pc.arp_table.get_mac(destination_pc.ip) != destination_pc.mac:
            broadcast_waves = self.build_broadcast_waves(source_item, destination_item)
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
            self.learn_switch_mac_along_path(source_pc.mac, broadcast_path)
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
                for cable, from_item, to_item in reverse_path
            )
            self.learn_switch_mac_along_path(destination_pc.mac, reverse_path)
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
        self.learn_switch_mac_along_path(source_pc.mac, path)

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
            for cable, from_item, to_item in reverse_path
        )
        self.learn_switch_mac_along_path(destination_pc.mac, reverse_path)
        return steps
