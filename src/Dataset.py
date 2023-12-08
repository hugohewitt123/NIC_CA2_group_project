import Node
# Params, Nodes and Items of the problem

class Dataset:
    def __init__(self):
        self.dimension = -1  # Num of cities
        self.num_of_items = -1
        self.knapsack_cap = -1
        self.min_speed = -1
        self.max_speed = -1
        self.renting_ration = -1
        self.coord_x = []
        self.coord_y = []
        self.nodes: Node = [None]
        self.items = []
