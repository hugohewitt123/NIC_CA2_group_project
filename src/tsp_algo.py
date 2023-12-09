import file_util as fu
import path_util as pu
import three_opt
import plotter
import Node
import Dataset
import Route
import datetime


"""
    function: random_three_opt
    description: do 3-opt evaluation for N rounds
    params:
        path (Node list): the original path
        evaluations (int): rounds of evaluation
    return:
        n_path: new optimised path
"""
def random_three_opt(ds: Dataset, route: Route, evaluations: int):
    n_path: list = route.path.copy()
    for i in range(evaluations):
        if i % 500 == 0 or i == evaluations-1:
            dist = pu.get_path_dist(route.path)
            print(f"evaluations: {i} dist: {dist}")
        three_sections, route = three_opt.cut_three_rand_path(route, ds)
        route.path = three_opt.three_opt_swap(three_sections[0], three_sections[1], three_sections[2])

    print("random_three_opt done")
    return route.path, route


def local_three_opt(ds: Dataset, route: Route):
    n_path: list = route.path.copy()
    nodes: list = ds.nodes.copy()
    nodes = nodes[1:]
    for i in range(len(nodes)):
        if i % 100 == 0:
            print(f"idx: {i}")
        node = nodes[i]
        three_sections = three_opt.cut_three_consecutive_path(route, node)
        route.path = three_opt.three_opt_swap(three_sections[0], three_sections[1], three_sections[2])
    return route.path, route


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
    t_ds.nodes = original_path.copy()
    t_random_path = pu.get_random_path(t_ds)
    path_dist = pu.get_path_dist(t_random_path)
    print("old path dist", path_dist)

    t_random_path = random_three_opt(t_ds, t_random_path, 40)
    path_dist = pu.get_path_dist(t_random_path)
    print("new path dist", path_dist)


def test2():
    ct = datetime.datetime.now()
    print("start current time:-", ct)

    ds: Dataset = fu.file_reader(3)
    random_path = pu.get_random_path(ds)
    path_dist = pu.get_path_dist(random_path)
    print("old path dist", path_dist)

    # Note: A normal 3-opt would take (n k) = n!/(k!(n-k)!) tries
    # This version will only take "n" evaluation rounds defined by user

    route = Route.Route(random_path, [], 10000)
    random_path, route = local_three_opt(ds, route)
    # random_path, route = random_three_opt(ds, route, 10000)
    path_dist = pu.get_path_dist(random_path)
    print("new path dist", path_dist)

    ct = datetime.datetime.now()
    print("end current time:-", ct)


# test1()
test2()
print("Done")

