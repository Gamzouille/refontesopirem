def should_forward_arp_broadcast(self, current_item, next_item, destination_item):
        if not hasattr(current_item, "switch"):
            return True

        if hasattr(next_item, "switch"):
            return True

        if not hasattr(next_item, "pc"):
            return True

        if next_item is destination_item:
            return True

        return next_item.pc.mac not in current_item.switch.mac_table

def build_broadcast_waves(self, start_item, destination_item):
        current_wave = [start_item]
        visited = {start_item}
        waves = []

        while current_wave:
            next_wave = []
            segments = []

            for current_item in current_wave:
                for cable in self.cables:
                    if cable.item1 is current_item:
                        next_item = cable.item2
                    elif cable.item2 is current_item:
                        next_item = cable.item1
                    else:
                        continue

                    if not self.should_forward_arp_broadcast(current_item, next_item, destination_item):
                        continue

                    if next_item in visited:
                        continue

                    visited.add(next_item)
                    next_wave.append(next_item)
                    segments.append((cable, current_item, next_item))

            if segments:
                waves.append(segments)
            current_wave = next_wave

        return waves

def build_broadcast_path(self, start_item):
        queue = [(start_item, [])]
        visited = {start_item}
        broadcast_path = []

        while queue:
            current_item, _current_path = queue.pop(0)
            for cable in self.cables:
                if cable.item1 is current_item:
                    next_item = cable.item2
                elif cable.item2 is current_item:
                    next_item = cable.item1
                else:
                    continue

                if next_item in visited:
                    continue

                visited.add(next_item)
                queue.append((next_item, []))
                broadcast_path.append((cable, current_item, next_item))

        return broadcast_path