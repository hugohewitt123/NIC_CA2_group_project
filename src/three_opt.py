import file_util as fu
import path_util as pu
import plotter
import Node
import Dataset
import random


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


def cut_three_path(path: list):
    idx = []
    for i in range(len(path)):
        idx.append(i)
    selected_nodes = random.sample(idx, 3)
    selected_nodes.sort()
    node_sections: list = [None] * 3
    node_sections[0] = path[selected_nodes[0]:selected_nodes[1]]
    node_sections[1] = path[selected_nodes[1]:selected_nodes[2]]
    if selected_nodes[0] == 0:
        node_sections[2] = path[selected_nodes[2]:]
    else:
        node_sections[2] = path[selected_nodes[2]:] + path[:selected_nodes[0]]
    # for i in range(3):
    #    pu.print_path_order(node_sections[i])
    return node_sections
