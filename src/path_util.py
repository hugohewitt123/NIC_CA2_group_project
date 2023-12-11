import Dataset
import Node
import math
import datetime
import random


"""
    WARNING!!! DO NOT RUN THIS FUNCTION IN THE LARGEST DATA SET
    function: get_dist_matrix (DEPRECATED)
    description: get distance between every nodes
    params:
        ds (Dataset): the dataset
    return:
        dist_matrix: Distance matrix in from of 2D array. Each node correspond to the node Id
"""
def get_dist_matrix(ds: Dataset):  # DEPRECATED
    print(datetime.datetime.now(), "get matrix")
    dimension: int = 0
    dimension = ds.dimension + 1
    dist_matrix = [[0.0 for i in range(dimension)] for i in range(dimension)]

    print(datetime.datetime.now(), "finished init")
    nodes: Node = ds.nodes
    for i in range(dimension):
        if i % 1000 == 0:
            print("round:", i)
        for j in range(dimension):
            if dist_matrix[j][i] != 0 or i == 0 or j == 0:
                continue
            elif i == j:
                dist_matrix[i][j] = 0.0
            else:
                dist_matrix[i][j] = cal_dist(nodes[i], nodes[j])
                dist_matrix[j][i] = cal_dist(nodes[i], nodes[j])
    print(datetime.datetime.now(), "dist matrix ready")
    return dist_matrix


"""
    function: get_random_path
    description: generate a random path for initialization
    params:
        ds (Dataset): The Dataset
    return:
        The path in the form of List (Node)
"""
def get_random_path(ds: Dataset):
    length = 0
    nodes_pool = ds.nodes.copy()
    if nodes_pool[0] is None:
        # From Real Dataset
        nodes = nodes_pool[1:]
        length = len(nodes_pool)-1
    else:
        # From Test Nodes
        nodes = nodes_pool
        length = len(nodes_pool)

    path: Node = []
    for i in range(length):
        rand_num = random.randint(0, len(nodes)-1)
        path.append(nodes[rand_num])
        del nodes[rand_num]
    return path


"""
    function: get_path_dist
    description: calculate total distance of the path
    params:
        path (List: Node): The path
    return:
        Total distance in float
"""
def get_path_dist(path: list):
    total_dist: float = 0.0
    for i in range(len(path)):
        node: Node = path[i]
        if i < (len(path) - 1):
            next_node: Node = path[i + 1]
            total_dist += cal_dist(node, next_node)
        else:
            next_node: Node = path[0]
            total_dist += cal_dist(node, next_node)
    return total_dist


"""
    function: cal_dist
    description: calculate distance between 2 nodes
    params:
        node_a (Node): first node
        node_b (Node): second node
    return:
        distance of two nodes in float 3 decimal places
"""
def cal_dist(node_a: Node, node_b: Node):
    dist: float = math.sqrt(abs(node_a.coord_x - node_b.coord_x)**2 + abs(node_a.coord_y - node_b.coord_y)**2)
    return round(dist, 3)


"""
    function: print_path_order
    description: print node number in a node list
    params:
        path (Node list): the node list
"""
def print_path_order(path: list):
    for node in path:
        if isinstance(node, Node.Node):
            print(node.node_id, end=" ")
        else:
            print(node, end=" ")
    print("")


"""
    function: node_to_node_index
    description: from node to node index number list
    params:
        indexes: the node index number list
"""
def node_to_node_index(path: list):
    indexes = []
    for node in path:
        indexes.append(node.node_id)
    return indexes
