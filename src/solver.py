import Params
import tsp_algo
import file_util as fu
from src import TSP_Data

the_param: Params = fu.read_param_properties()
tsp_graph_data = TSP_Data.TSP_Data()
tsp_population, tsp_graph_data = tsp_algo.tsp_solve(the_param.dataset_idx, the_param)
print("Done")
