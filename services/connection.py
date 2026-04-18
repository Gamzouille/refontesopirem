def disconnect_cable(self, cable):
        item1 = cable.item1
        item2 = cable.item2
        p1 = cable.get_port_for_item(item1)
        p2 = cable.get_port_for_item(item2)

        if hasattr(item1, "switch") and p1 is not None:
            if hasattr(item2, "pc"):
                item1.switch.ports[p1] = None
                if item2.pc.switch is item1.switch and item2.pc.switch_port == p1:
                    item2.pc.switch = None
                    item2.pc.switch_port = None
            elif hasattr(item2, "switch"):
                item1.switch.uplink_ports = getattr(item1.switch, "uplink_ports", set())
                item1.switch.uplink_ports.discard(p1)

        if hasattr(item2, "switch") and p2 is not None:
            if hasattr(item1, "pc"):
                item2.switch.ports[p2] = None
                if item1.pc.switch is item2.switch and item1.pc.switch_port == p2:
                    item1.pc.switch = None
                    item1.pc.switch_port = None
            elif hasattr(item1, "switch"):
                item2.switch.uplink_ports = getattr(item2.switch, "uplink_ports", set())
                item2.switch.uplink_ports.discard(p2)

        if cable in item1.cables:
            item1.cables.remove(cable)
        if cable in item2.cables:
            item2.cables.remove(cable)
        if cable in self.cables:
            self.cables.remove(cable)
        if cable.scene() is not None:
            self.scene.removeItem(cable)

def disconnect_machine(self, item):
        for cable in list(self.cables):
            if cable.item1 is item or cable.item2 is item:
                self.disconnect_cable(cable)
def apply_connection_config(self, item1, item2, config):
        s1 = item1.switch if hasattr(item1, "switch") else None
        s2 = item2.switch if hasattr(item2, "switch") else None
        pc1 = item1.pc if hasattr(item1, "pc") else None
        pc2 = item2.pc if hasattr(item2, "pc") else None

        if s1 is not None:
            p1 = config.get("switch1_port")
            occupied = s1.ports.get(p1)
            if occupied is not None and occupied is not pc2:
                QMessageBox.warning(self, "Port occupe", f"Le port {p1} de {s1.nom} est deja utilise.")
                return False
            if p1 in getattr(s1, "uplink_ports", set()):
                QMessageBox.warning(self, "Port occupe", f"Le port {p1} de {s1.nom} est deja utilise.")
                return False

        if s2 is not None:
            p2 = config.get("switch2_port")
            occupied = s2.ports.get(p2)
            if occupied is not None and occupied is not pc1:
                QMessageBox.warning(self, "Port occupe", f"Le port {p2} de {s2.nom} est deja utilise.")
                return False
            if p2 in getattr(s2, "uplink_ports", set()):
                QMessageBox.warning(self, "Port occupe", f"Le port {p2} de {s2.nom} est deja utilise.")
                return False

        if s1 is not None and pc2 is not None:
            if pc2.switch is not None and pc2.switch is not s1:
                QMessageBox.warning(self, "PC deja connecte", f"{pc2.name} est deja connecte a {pc2.switch.nom}.")
                return False
            if pc2.switch is s1 and pc2.switch_port != config["switch1_port"] and pc2.switch_port in s1.ports:
                s1.ports[pc2.switch_port] = None
            s1.connect(config["switch1_port"], pc2)
            return True

        if s2 is not None and pc1 is not None:
            if pc1.switch is not None and pc1.switch is not s2:
                QMessageBox.warning(self, "PC deja connecte", f"{pc1.name} est deja connecte a {pc1.switch.nom}.")
                return False
            if pc1.switch is s2 and pc1.switch_port != config["switch2_port"] and pc1.switch_port in s2.ports:
                s2.ports[pc1.switch_port] = None
            s2.connect(config["switch2_port"], pc1)
            return True

        if s1 is not None and s2 is not None:
            if s1 is s2:
                QMessageBox.warning(self, "Connexion invalide", "Impossible de connecter un switch a lui-meme.")
                return False
            if not hasattr(s1, "uplink_ports"):
                s1.uplink_ports = set()
            if not hasattr(s2, "uplink_ports"):
                s2.uplink_ports = set()
            s1.uplink_ports.add(config["switch1_port"])
            s2.uplink_ports.add(config["switch2_port"])
            return True

        return True

def build_connections_text(self, item):
        lines = []
        for cable in self.cables:
            if cable.item1 is item:
                other = cable.item2
            elif cable.item2 is item:
                other = cable.item1
            else:
                continue

            other_type = "PC" if hasattr(other, "pc") else "Switch" if hasattr(other, "switch") else "Appareil"
            other_name = self.get_device_name(other)
            own_port = cable.get_port_for_item(item)
            other_port = cable.get_port_for_item(other)

            line = f"- {other_type} {other_name}"
            port_chunks = []
            if hasattr(item, "switch") and own_port is not None:
                port_chunks.append(f"port local: {own_port}")
            if hasattr(other, "switch") and other_port is not None:
                port_chunks.append(f"port distant (switch): {other_port}")
            if port_chunks:
                line += " | " + " | ".join(port_chunks)
            lines.append(line)

        if not lines:
            return "Aucune connexion"
        return "\n".join(lines)

def get_cable_details_for_item(self, item):
        details = []
        for cable in self.cables:
            if cable.item1 is item:
                other = cable.item2
            elif cable.item2 is item:
                other = cable.item1
            else:
                continue
            details.append({
                "cable": cable,
                "other": other,
                "own_port": cable.get_port_for_item(item),
                "other_port": cable.get_port_for_item(other),
            })
        return details