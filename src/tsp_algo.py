import file_util as fu
import path_util as pu
import three_opt
import plotter
import Node
import Dataset
import random


"""
    function: random_three_opt
    description: do 3-opt evaluation for N rounds
    params:
        path (Node list): the original path
        evaluations (int): rounds of evaluation
    return:
        n_path: new optimised path
"""
def random_three_opt(path: list, evaluations: int):
    n_path: list = path.copy()
    for i in range(evaluations):
        if i % 500 == 0 or i == evaluations-1:
            dist = pu.get_path_dist(n_path)
            print(f"evaluations: {i} dist: {dist}")
        three_sections: list = three_opt.cut_three_path(n_path)
        n_path = three_opt.three_opt_swap(three_sections[0], three_sections[1], three_sections[2])

    print("random_three_opt done")
    return n_path


# Test Section
def test1():
    node_1 = Node.Node(2, 6, 1, None)  # A
    node_2 = Node.Node(5, 8, 2, None)  # B
    node_3 = Node.Node(8, 6, 3, None)  # C
    node_4 = Node.Node(8, 3, 4, None)  # D
    node_5 = Node.Node(5, 1, 5, None)  # E
    node_6 = Node.Node(2, 3, 6, None)  # F

    original_path = [node_1, node_2, node_3, node_4, node_5, node_6]

    t_ds = Dataset.Dataset()
    t_ds.nodes = original_path
    t_random_path = pu.get_random_path(t_ds)
    path_dist = pu.get_path_dist(t_random_path)
    print("old path dist", path_dist)

    t_random_path = random_three_opt(t_random_path, 5)
    path_dist = pu.get_path_dist(t_random_path)
    print("new path dist", path_dist)


def test2():
    ds: Dataset = fu.file_reader(0)
    random_path = pu.get_random_path(ds)
    path_dist = pu.get_path_dist(random_path)
    print("old path dist", path_dist)

    random_path = random_three_opt(random_path, 10000)
    path_dist = pu.get_path_dist(random_path)
    print("new path dist", path_dist)


# test1()
test2()
print("Done")

