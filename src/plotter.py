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
    coords_x = [dataset.coord_x[1:len(dataset.coord_x)]]
    coords_y = [dataset.coord_y[1:len(dataset.coord_x)]]
    plt.scatter(coords_x, coords_y, s=0.5)
    plt.show()


# Testing Section
ds = fu.file_reader(1)
plot_distribution(None, ds)
