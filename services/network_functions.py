

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





