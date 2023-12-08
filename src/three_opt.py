import file_util as fu
import path_util as pu
import plotter
import Node


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

    plot_all_3opts(three_opt_paths)

    return find_best_path(three_opt_paths)


def reverse_path(path: list):
    r_path: Node = []
    for i in range(len(path)):
        r_path.append(path[len(path)-i-1])
    return r_path


def plot_all_3opts(paths: list):
    for i in range(len(paths)):
        dist = round(pu.get_path_dist(paths[i]), 2)
        title = f"option {i} total dist {dist}"
        plotter.plot_path(paths[i], None, 2, title=title)


def find_best_path(paths: list):
    lowest = -1
    idx = -1
    for i in range(len(paths)):
        current = pu.get_path_dist(paths[i])
        if lowest == -1 or current < lowest:
            lowest = current
            idx = i
    print("best path", idx)
    return paths[idx]


node_1 = Node.Node(2, 6, 1, None)
node_2 = Node.Node(5, 8, 2, None)
node_3 = Node.Node(8, 6, 3, None)
node_4 = Node.Node(8, 3, 4, None)
node_5 = Node.Node(5, 1, 5, None)
node_6 = Node.Node(2, 3, 6, None)

original_path = [node_1, node_2, node_3, node_4, node_5, node_6]
path_dist = pu.get_path_dist(original_path)
path_reverse = reverse_path([node_1, node_2])
print("path_dist", path_dist)

new_path = three_opt_swap(original_path[0:2], original_path[2:4], original_path[4:6])
print("Done")
