import Dataset
import Node


def get_dist_matrix(ds: Dataset):
    dist_matrix = [[None]*ds.dimension]
    for i in range(ds.dimension):
        for j in range(ds.dimension):
            if i == j:
                print(123)


def cal_dist(node_a: Node, node_b: Node):
    print(123)
