import matplotlib.pyplot as plt
import Dataset
import file_util as fu

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
    plt.figure(figsize=(14,10))
    plt.scatter(coords_x, coords_y, c=node_items_highest_profit_ratio, s=20, cmap='viridis')
    plt.colorbar()
    plt.show()


# Testing Section
ds = fu.file_reader(2)
plot_distribution(None, ds)
