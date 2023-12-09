import Dataset
import Node
import file_util
import math
import datetime
import random


# WARNING!!! DO NOT RUN THIS FUNCTION IN THE LARGEST DATA SET
def get_dist_matrix(ds: Dataset):
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
    description: generate a random path of initialization
    params:
        ds (Dataset): The Dataset
    return:
        The path in the form of List (Node)
"""
def get_random_path(ds: Dataset):
    nodes = ds.nodes[1:]
    path: Node = []
    for i in range(len(ds.nodes)-1):
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


# Testing Section
#dataset: Dataset = file_util.file_reader(0)
#test_path = get_random_path(dataset)
#test_path_dist = get_path_dist(test_path)
# get_dist_matrix(dataset) # DONT PUT LARGEST DATASET
