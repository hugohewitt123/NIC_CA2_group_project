import file_util as fu
import path_util as pu
import plotter
import Node
import Route
import Dataset
import random
import math
from warnings import warn

"""
    function: three_opt_swap
    description: three_opt_swap from 3 node list
    params:
        path_1 (Node: list): path section 1
        path_2 (Node: list): path section 2
        path_3 (Node: list): path section 3
    return:
        new_best_path: best 3-opt path in Node list
        new_best_dist:  distance of best path
"""
def three_opt_swap(path_1: list, path_2: list, path_3: list):
    three_opt_paths = []
    dist_simplified = []
    r_path_2 = reverse_path(path_2)
    r_path_3 = reverse_path(path_3)

    # 1, 2, 3, 1
    path_option_1 = path_1 + path_2 + path_3
    three_opt_paths.append(path_option_1)
    temp_dist: float = (pu.cal_dist(path_1[-1], path_2[0])
                        + pu.cal_dist(path_2[-1], path_3[0])
                        + pu.cal_dist(path_3[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 2', 3', 1
    path_option_2 = path_1 + r_path_2 + r_path_3
    three_opt_paths.append(path_option_2)
    temp_dist: float = (pu.cal_dist(path_1[-1], r_path_2[0])
                        + pu.cal_dist(r_path_2[-1], r_path_3[0])
                        + pu.cal_dist(r_path_3[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 2', 3, 1
    path_option_3 = path_1 + r_path_2 + path_3
    three_opt_paths.append(path_option_3)
    temp_dist: float = (pu.cal_dist(path_1[-1], r_path_2[0])
                        + pu.cal_dist(r_path_2[-1], path_3[0])
                        + pu.cal_dist(path_3[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 3, 2, 1
    path_option_4 = path_1 + path_3 + path_2
    three_opt_paths.append(path_option_4)
    temp_dist: float = (pu.cal_dist(path_1[-1], path_3[0])
                        + pu.cal_dist(path_3[-1], path_2[0])
                        + pu.cal_dist(path_2[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 3, 2', 1
    path_option_5 = path_1 + path_3 + r_path_2
    three_opt_paths.append(path_option_5)
    temp_dist: float = (pu.cal_dist(path_1[-1], path_3[0])
                        + pu.cal_dist(path_3[-1], r_path_2[0])
                        + pu.cal_dist(r_path_2[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 3', 2', 1
    path_option_6 = path_1 + r_path_3 + r_path_2
    three_opt_paths.append(path_option_6)
    temp_dist: float = (pu.cal_dist(path_1[-1], r_path_3[0])
                        + pu.cal_dist(r_path_3[-1], r_path_2[0])
                        + pu.cal_dist(r_path_2[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # 1, 3', 2, 1
    path_option_7 = path_1 + r_path_3 + path_2
    three_opt_paths.append(path_option_7)
    temp_dist: float = (pu.cal_dist(path_1[-1], r_path_3[0])
                        + pu.cal_dist(r_path_3[-1], path_2[0])
                        + pu.cal_dist(path_2[-1], path_1[0]))
    dist_simplified.append(temp_dist)

    # plot_all_3opts(three_opt_paths)

    # This line is old code but still works (But very slow)
    """
    best_path, best_path_dist = find_best_path(three_opt_paths)
    return best_path, best_path_dist
    """

    new_lowest_dist_idx = dist_simplified.index(min(dist_simplified))
    new_best_path = three_opt_paths[new_lowest_dist_idx]
    new_best_dist = pu.get_path_dist(three_opt_paths[new_lowest_dist_idx])
    return new_best_path, new_best_dist


"""
    function: reverse_path
    description: put the Node list in reverse order
    params:
        path (Node: list): the path
    return:
        r_path: path in reverse order
"""
def reverse_path(path: list):
    r_path: Node = []
    for i in range(len(path)):
        r_path.append(path[len(path)-i-1])
    return r_path


"""
    function: plot_all_3opts
    description: show all path options in graph (visualisation)
    params:
        path (Node: list: list): the path
"""
def plot_all_3opts(paths: list):
    for i in range(len(paths)):
        dist = round(pu.get_path_dist(paths[i]), 2)
        title = f"option {i+1} total dist {dist}"
        plotter.plot_path(paths[i], None, 2, title=title)


"""
    function: find_best_path (DEPRECATED)
    description: find best path for 3-opts, already integrated into three_opt_swap
    params:
        path (Node: list: list): list of paths
    return:        
        paths[idx]: the best path (lowest distance)
        lowest_dist: the distance of the best path
"""
def find_best_path(paths: list):  # DEPRECATED
    warn('This is deprecated', DeprecationWarning, stacklevel=2)
    lowest = -1
    idx = -1
    for i in range(len(paths)):
        current = pu.get_path_dist(paths[i])
        if lowest == -1 or current < lowest:
            lowest = current
            idx = i
    # print("best path", idx)
    lowest_dist = pu.get_path_dist(paths[idx])
    return paths[idx], lowest_dist


"""
    function: cut_three_rand_path
    description: cut 3 edges from the path and update the optimised 3-opt record in Route
    params:
        route (Route): the Route object
        ds (Dataset): the Dataset object
    return:
        node_sections: 3 paths in Node lists
        route: updated record
"""
def cut_three_rand_path(route: Route, ds: Dataset):
    path = route.path
    idx = ds.nodes.copy()
    idx = idx[1:]

    selected_nodes = random.sample(idx, 3)

    for i in range(len(selected_nodes)):
        if (selected_nodes[i].node_id is None) or (selected_nodes[i] is None):
            print("pause")

    selected_nodes.sort(key=lambda x: x.node_id, reverse=False)
    record_counter = len(route.three_opt_record)
    combinations = math.comb(len(idx), 3)
    while (route.check_repeat_combination(selected_nodes) and
           record_counter < route.evaluation_rounds and
           record_counter < combinations):
        selected_nodes = random.sample(idx, 3)
        selected_nodes.sort(key=lambda x: x.node_id, reverse=False)
    if not route.check_repeat_combination(selected_nodes):
        route.append_record(selected_nodes)

    selected_nodes_idx = pu.node_to_node_index(selected_nodes)
    node_sections: list = [None] * 3
    node_sections[0] = path[selected_nodes_idx[0]:selected_nodes_idx[1]]
    node_sections[1] = path[selected_nodes_idx[1]:selected_nodes_idx[2]]
    if selected_nodes_idx[2] == 0:
        node_sections[2] = path[selected_nodes_idx[2]:]
    else:
        node_sections[2] = path[selected_nodes_idx[2]:] + path[:selected_nodes_idx[0]]

    return node_sections, route


"""
    function: cut_three_rand_path
    description: cut 3 alternating consecutive edges from the path
    params:
        route (Route): the Route object
        node (Node): the Node object
    return:
        path_sections: 3 paths in Node lists
"""
def cut_three_consecutive_path(route: Route, node: Node):
    path = route.path.copy()
    # path = [0,1,2,3,4,5,6,7,8]
    path_len = len(path)
    if node in path:
        idx = path.index(node)
    else:
        print("pause")
    # idx = 4
    path_sections = [None] * 3
    path_sections[0] = get_section(path, (idx) % path_len, (idx+2) % path_len)
    path_sections[1] = get_section(path, (idx+2) % path_len, (idx+4) % path_len)
    path_sections[2] = get_section(path, (idx+4) % path_len, (idx) % path_len)

    return path_sections


"""
    function: get_section (DEPRECATED)
    description: handle list that loop around
    params:
        path (list): any type of list
        start (int): starting index
        end (int): ending index
    return:
        path[start:] + path[:end]: the section of the list needed
"""
def get_section(path, start, end):
    if start < end:
        return path[start:end]
    else:
        return path[start:] + path[:end]

