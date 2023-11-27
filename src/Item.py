# Item object for ITEMS SECTION

class Item:
    """
        constructor
        params:
            profit: profit
            weight: weight
            node: assigned node number
    """
    def __init__(self, profit, weight, node):
        self.profit = profit
        self.weight = weight
        self.assigned_node = node
