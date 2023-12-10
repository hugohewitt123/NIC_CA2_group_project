import Node

"""
    class: Route
    description: individual instance (population) in TSP
    params:
        path (node: list): the TSP path
        three_opt_record (node: list: list): 3-opt combination that had gone through
        evaluation_rounds (int): round of fitness evaluation (times of 3-opt that will do in a random 3-opt optimisation)
"""
class Route:
    def __init__(self, path: list, three_opt_record: list, evaluation_rounds: int):
        self.path: list = path
        self.three_opt_record: list = three_opt_record
        self.evaluation_rounds = evaluation_rounds

    """
        function: check_repeat_combination
        description: check the selected combination did 3-opt or not
        params:
            combi (Node list): selected combination for 3-opt
        return:
            boolean value
    """
    def check_repeat_combination(self, combi: list):
        combi.sort(key=lambda x: x.node_id, reverse=False)
        if combi in self.three_opt_record:
            return True
        else:
            return False

    """
        function: append_record
        description: add new record sort in node_id
        params:
            combi (Node list): selected combination for 3-opt
        return:
            length of the record
    """
    def append_record(self, combi: list):
        combi.sort(key=lambda x: x.node_id, reverse=False)
        self.three_opt_record.append(combi)
        return len(self.three_opt_record)


# Test Section
"""
node_1 = Node.Node(2, 6, 1, None)  # A
node_2 = Node.Node(5, 8, 2, None)  # B
node_3 = Node.Node(8, 6, 3, None)  # C
tuple_a = [node_1, node_2, node_3]
tuple_b = [node_3, node_2, node_1]
tuple_a.sort(key=lambda x: x.node_id, reverse=False)
tuple_b.sort(key=lambda x: x.node_id, reverse=False)

r = Route([], [[node_1, node_2, node_3]])
print(r.check_repeat_combination(tuple_b))
"""

