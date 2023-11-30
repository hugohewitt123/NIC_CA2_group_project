# Item object for ITEMS SECTION

class Item:
    """
        constructor
        params:
            profit: profit
            weight: weight
            node: assigned node number
    """
    def __init__(self, index, profit, weight, node):
        self.index = index
        self.profit = profit
        self.weight = weight
        self.assigned_node = node
        self.profit_ratio = profit / weight
