# Node object for nodes section

class Node:
    def __init__(self, coord_x, coord_y, node_id, items):
        self.node_id: int = node_id
        self.coord_x: float = coord_x
        self.coord_y: float = coord_y
        if items is None:
            self.items = []
        elif len(items) == 0:
            self.items = []
        else:
            self.items.append(items)

    def sort_item_profit_ratio(self):
        self.items.sort(key=lambda x: x.profit_ratio, reverse=True)
