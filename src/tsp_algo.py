import file_util as fu
import path_util as pu
import three_opt
import plotter
import Params
import TSP_Data
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
        route.path: new optimised path
        route: Route object
"""
def random_three_opt(ds: Dataset, route: Route, evaluations: int, graph_data: TSP_Data):
    n_path: list = route.path.copy()
    print("evaluations, dist")

    start_path_dist = pu.get_path_dist(n_path)
    print(0, start_path_dist)
    graph_data.add_data(0, start_path_dist)

    for i in range(evaluations):
        three_sections, route = three_opt.cut_three_rand_path(route, ds)
        route.path, p_dist = three_opt.three_opt_swap(three_sections[0].copy(), three_sections[1].copy(),
                                                      three_sections[2].copy())
        if (i % 100 == 0 or i == evaluations - 1) and i != 0:
            print(f"{i}, {p_dist}")
            graph_data.add_data(i, p_dist)

    print("random_three_opt done")
    return route.path, route


"""
    function: local_three_opt
    description: do 3-opt optimise every node
    params:
        ds (Dataset): the Dataset object
        route (Route): the Route object
        evaluations (int): round of random evaluation needed
        graph_data (TSP_Data): for generating graphs for data visualisation
    return:
        route.path: optimal path after N-time evaluations
        route: Route object
"""
def local_three_opt(ds: Dataset, route: Route, evaluations: int, graph_data: TSP_Data):
    n_path: list = route.path.copy()
    nodes: list = ds.nodes.copy()
    nodes = nodes[1:]
    print("idx, dist")
    for i in range(len(nodes)):
        node = nodes[i]
        three_sections = three_opt.cut_three_consecutive_path(route, node)
        route.path, p_dist = three_opt.three_opt_swap(three_sections[0], three_sections[1], three_sections[2])

        if i % 100 == 0 or i == (len(nodes) - 1):
            print(f"{i+evaluations},{p_dist}")
            graph_data.add_data((i+evaluations), p_dist)

    print("local_three_opt done")
    return route.path, route


"""
    function: tsp_solve
    description: implementation of the TSP solver
    params:
        file_idx (int)
        param (Params)
    return:
        path_population: node lists of path after 3-opt
        tsp_graph_data: for plotting graphs
"""
def tsp_solve(file_idx: int, param: Params):
    ct = datetime.datetime.now()
    print("tsp start time:-", ct)

    path_population = []
    tsp_graph_data = TSP_Data.TSP_Data()

    ds: Dataset = fu.file_reader(file_idx)
    for i in range(param.population_size_nsg):
        random_path = pu.get_random_path(ds)

        # Note: A normal 3-opt would take (n k) = n!/(k!(n-k)!) tries
        # This version will only take "n" evaluation rounds defined by user

        evaluations = param.evaluations_tsp

        route = Route.Route(random_path, [], evaluations)

        # Random 3-opt
        random_path, route = random_three_opt(ds, route, evaluations, tsp_graph_data)

        # Local 3-opt, goes through all the nodes
        if param.run_local_tsp:
            random_path, route = local_three_opt(ds, route, evaluations, tsp_graph_data)

        path_population.append(random_path)

        path_dist = pu.get_path_dist(random_path)
        print("end", path_dist, "\n")

    ct = datetime.datetime.now()
    print("tsp end time:-", ct)

    return path_population, tsp_graph_data


"""
    function: test1 (DEPRECATED)
    description: testing and debug only
"""
# Test Section
def test1():
    node_1 = Node.Node(2, 6, 1, None)  # A
    node_2 = Node.Node(5, 8, 2, None)  # B
    node_3 = Node.Node(8, 6, 3, None)  # C
    node_4 = Node.Node(8, 3, 4, None)  # D
    node_5 = Node.Node(5, 1, 5, None)  # E
    node_6 = Node.Node(2, 3, 6, None)  # F

    original_path = [node_1, node_2, node_3, node_4, node_5, node_6]

    evaluations = 10
    t_ds = Dataset.Dataset()
    t_ds.nodes = original_path.copy()
    t_random_path = pu.get_random_path(t_ds)
    route = Route.Route(t_random_path, [], evaluations)

    path_dist = pu.get_path_dist(t_random_path)
    print("old path dist", path_dist)

    t_random_path, route = random_three_opt(t_ds, t_random_path, evaluations)
    path_dist = pu.get_path_dist(t_random_path)
    print("new path dist", path_dist)
