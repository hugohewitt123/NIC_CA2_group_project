import file_util as fu
import path_util as pu
import plotter
import Node
import Route
import Dataset
import random
import math


def three_opt_swap(path_1: list, path_2: list, path_3: list):
    three_opt_paths = []
    # 1, 2, 3, 1
    path_option_1 = path_1 + path_2 + path_3
    three_opt_paths.append(path_option_1)
    # 1, 2', 3', 1
    path_option_2 = path_1 + reverse_path(path_2) + reverse_path(path_3)
    three_opt_paths.append(path_option_2)
    # 1, 2', 3, 1
    path_option_3 = path_1 + reverse_path(path_2) + path_3
    three_opt_paths.append(path_option_3)
    # 1, 3, 2, 1
    path_option_4 = path_1 + path_3 + path_2
    three_opt_paths.append(path_option_4)
    # 1, 3, 2', 1
    path_option_5 = path_1 + path_3 + reverse_path(path_2)
    three_opt_paths.append(path_option_5)
    # 1, 3', 2', 1
    path_option_6 = path_1 + reverse_path(path_3) + reverse_path(path_2)
    three_opt_paths.append(path_option_6)
    # 1, 3', 2, 1
    path_option_7 = path_1 + reverse_path(path_3) + path_2
    three_opt_paths.append(path_option_7)

    # plot_all_3opts(three_opt_paths)

    return find_best_path(three_opt_paths)


def reverse_path(path: list):
    r_path: Node = []
    for i in range(len(path)):
        r_path.append(path[len(path)-i-1])
    return r_path


def plot_all_3opts(paths: list):
    for i in range(len(paths)):
        dist = round(pu.get_path_dist(paths[i]), 2)
        title = f"option {i+1} total dist {dist}"
        plotter.plot_path(paths[i], None, 2, title=title)


def find_best_path(paths: list):
    lowest = -1
    idx = -1
    for i in range(len(paths)):
        current = pu.get_path_dist(paths[i])
        if lowest == -1 or current < lowest:
            lowest = current
            idx = i
    # print("best path", idx)
    return paths[idx]


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
    # for i in range(3):
    #    pu.print_path_order(node_sections[i])
    return node_sections, route


def cut_three_consecutive_path(route: Route, node: Node):
    path = route.path.copy()
    # path = [0,1,2,3,4,5,6,7,8]
    path_len = len(path)
    idx = path.index(node)
    # idx = 4
    path_sections = [None] * 3
    path_sections[0] = get_section(path, idx % path_len, idx+2 % path_len)
    path_sections[1] = get_section(path, idx+2 % path_len, idx+4 % path_len)
    path_sections[2] = get_section(path, idx+4 % path_len, idx % path_len)
    return path_sections


def get_section(path, start, end):
    if start < end:
        return path[start:end]
    else:
        return path[start:] + path[:end]

