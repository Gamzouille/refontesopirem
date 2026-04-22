def find_path_between_items(self, start_item, end_item):
        if start_item is end_item:
            return []

        queue = [(start_item, [])]
        visited = {start_item}

        while queue:
            current_item, current_path = queue.pop(0)
            for cable in self.cables:
                if cable.item1 is current_item:
                    next_item = cable.item2
                elif cable.item2 is current_item:
                    next_item = cable.item1
                else:
                    continue

                if next_item in visited:
                    continue

                next_path = current_path + [(cable, current_item, next_item)]
                if next_item is end_item:
                    return next_path

                visited.add(next_item)
                queue.append((next_item, next_path))

        return None

def reverse_path(self, path):
        return [(cable, to_item, from_item) for cable, from_item, to_item in reversed(path)]