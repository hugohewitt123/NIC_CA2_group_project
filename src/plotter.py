import Dataset
import Node
import file_util as fu
import path_util as pu
import matplotlib.pyplot as plt
import numpy as np

"""
    function name: plot_distribution
    params:
        file_name (str): file name in array
        dataset (Dataset): the dataset
"""
def plot_distribution(file_name, dataset):
    coords_x = [dataset.coord_x[1:]]
    coords_y = [dataset.coord_y[1:]]
    node_items_highest_profit_ratio = [0]
    for i, node in enumerate(dataset.nodes):
        if i > 1:
            node_items_highest_profit_ratio.append(node.items[0].profit_ratio)
    plt.figure(figsize=(14, 10))
    plt.scatter(coords_x, coords_y, c=node_items_highest_profit_ratio, s=20, cmap='viridis')
    plt.colorbar()
    plt.show()


"""
    function name: plot_path
    description:
    params:
        file_name (str): file name in array
        dataset (Dataset): the dataset
"""
def plot_path(path: list, dataset: Dataset, *line_width, **optionals):
    if len(line_width) == 0:
        line_width = 0.2
    else:
        line_width = line_width[0]

    plt.figure(figsize=(28, 20))
    plt.figure(figsize=(7, 5))
    for i in range(len(path)):
        if i < (len(path) - 1):
            node: Node = path[i]
            next_node: Node = path[i+1]
            x1: float = node.coord_x
            y1: float = node.coord_y
            x2: float = next_node.coord_x
            y2: float = next_node.coord_y
            plt.plot([x1, x2], [y1, y2], 'ro-', linewidth=line_width)
        else:
            node: Node = path[i]
            next_node: Node = path[0]
            x1: float = node.coord_x
            y1: float = node.coord_y
            x2: float = next_node.coord_x
            y2: float = next_node.coord_y
            plt.plot([x1, x2], [y1, y2], 'ro-', linewidth=line_width)
    title = optionals.get("title")
    if title != None:
        plt.title(title)
    else:
        plt.title("Path")
    plt.show()
