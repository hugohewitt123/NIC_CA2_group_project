# File reader puts text files into python objects
import Dataset
import Item
import Node
import Params
import os
import csv
from datetime import datetime

# script_dir = os.path.dirname(os.path.abspath(__file__))
# script_dir = script_dir.replace("\\", "/")
# folder = "/../resources/"
# folder_path = script_dir + folder
folder_path = './resources/'
# folder_path = "C:/Users/Lucas/Documents/Academic/Exeter/ECMM409 Nature Inspired Computation/CA2/CA2PY/resources/"
file_names = ["a280-n279", "a280-n1395", "a280-n2790",
              "fnl4461-n4460", "fnl4461-n22300", "fnl4461-n44600",
              "pla33810-n33809", "pla33810-n169045", "pla33810-n338090",
              "test-example-n4"]
param_file = "param_properties"
file_ext = ".txt"

"""
    function: reader
    description: put txt file into readable data for the program
    params:
        selected_file (int): indicates while file is currently reading in list "file_names"
    return:
        the dataset
"""
def file_reader(selected_file):
    full_path = folder_path + file_names[selected_file] + file_ext
    splitter = "\t"
    print("Reading:" + full_path)
    with open(full_path, mode='r') as f:
        lines = f.read().splitlines()
    dataset = Dataset.Dataset()
    dataset.dimension = int(lines[2].split(splitter)[1])
    dataset.num_of_items = int(lines[3].split(splitter)[1])
    dataset.knapsack_cap = float(lines[4].split(splitter)[1])
    dataset.min_speed = float(lines[5].split(splitter)[1])
    dataset.max_speed = float(lines[6].split(splitter)[1])
    dataset.renting_ration = float(lines[7].split(splitter)[1])

    # idx 0 not used in list
    dataset.coord_x.append(None)
    dataset.coord_y.append(None)
    node_line_offset = 10
    for i in range(dataset.dimension):
        node_id = int(lines[node_line_offset + i].split(splitter)[0])
        node_x = float(lines[node_line_offset + i].split(splitter)[1])
        node_y = float(lines[node_line_offset + i].split(splitter)[2])
        dataset.nodes.append(Node.Node(node_x, node_y, node_id, None))
        dataset.coord_x.append(node_x)
        dataset.coord_y.append(node_y)

    item_line_offset = node_line_offset + dataset.dimension + 1
    dataset.items = [None]#[[]] * (dataset.dimension + 1)
    # inx 0 not used in list
    dataset.items[0] = [None]
    for i in range(dataset.num_of_items):
        index = int(lines[item_line_offset + i].split(splitter)[0])
        profit = float(lines[item_line_offset + i].split(splitter)[1])
        weight = float(lines[item_line_offset + i].split(splitter)[2])
        assigned_node = int(lines[item_line_offset + i].split(splitter)[3])
        item = Item.Item(index, profit, weight, assigned_node)
        dataset.items.append(item)
        #node_items = dataset.items[assigned_node].copy()
        #node_items.append(item)
        #dataset.items[assigned_node] = node_items
        dataset.nodes[assigned_node].items.append(item)

    for i in range(len(dataset.nodes)):
        if i > 1:
            node = dataset.nodes[i]
            node.sort_item_profit_ratio()

    return dataset

def read_param_properties():
    full_path = folder_path + param_file + file_ext
    splitter = " "
    print("Reading:" + full_path)
    params = Params.Param()
    with open(full_path, mode='r') as f:
        lines = f.read().splitlines()
    params.population_size_nsg = int(lines[0].split(splitter)[1])
    params.evaluations_tsp = int(lines[1].split(splitter)[1])
    run_local_tsp_str = str(lines[2].split(splitter)[1]).lower()
    if run_local_tsp_str == 'true':
        params.run_local_tsp = True
    else:
        params.run_local_tsp = False
    params.tournament_size_ksp = int(lines[3].split(splitter)[1])
    params.num_generations_ksp = int(lines[4].split(splitter)[1])
    params.fill_rate_ksp = float(lines[5].split(splitter)[1])
    params.random_seed = int(lines[6].split(splitter)[1])
    params.exp_type = int(lines[7].split(splitter)[1])

    params.dataset_idx = int(lines[-1].split(splitter)[1])  # Last Index

    if params.population_size_nsg < params.tournament_size_ksp:
        raise Exception("Tournament of KSP size should be smaller than population size")

    return params

def write_results(final_population, hyper_volume, exp_local, dataset_local):
    output_dir = 'output_files'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_path = os.path.join(output_dir, f'dataset{dataset_local}_exp{exp_local}_{timestamp}.csv')

    time_values = [individual[0] for individual in final_population]
    profit_values = [individual[1] for individual in final_population]
    exp_locals = [exp_local] * len(hyper_volume)
    dataset_locals = [dataset_local] * len(hyper_volume)
    
    max_length = max(len(time_values), len(profit_values), len(hyper_volume))

    time_values.extend([''] * (max_length - len(time_values)))
    profit_values.extend([''] * (max_length - len(profit_values)))
    hyper_volume.extend([''] * (max_length - len(hyper_volume)))
    exp_locals.extend([''] * (max_length - len(exp_locals)))
    dataset_locals.extend([''] * (max_length - len(dataset_locals)))

    with open(output_file_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(['Time', 'Profit', 'Hypervolume', 'exp_type', 'dataset_idx'])
        writer.writerows(zip(time_values, profit_values, hyper_volume, exp_locals, dataset_locals))

def write_to_f_file(final_population, dataset_local):
    output_dir='output_files'
    os.makedirs(output_dir, exist_ok=True)

    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file_path = os.path.join(output_dir, f'group_M_{dataset_local}.f')

    with open(output_file_path, 'w') as f_file:
        for individual in final_population:
            time_value = individual[0]
            profit_value = individual[1]
            f_file.write(f'{time_value} {profit_value}\n')
