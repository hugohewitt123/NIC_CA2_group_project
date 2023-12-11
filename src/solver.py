import Params
import tsp_algo
import file_util as fu
import TSP_Data
import nsga_util

# The main program
the_param: Params = fu.read_param_properties()
tsp_graph_data = TSP_Data.TSP_Data()
tsp_population, tsp_graph_data = tsp_algo.tsp_solve(the_param.dataset_idx, the_param)
ds = fu.file_reader(the_param.dataset_idx)
#returns the final population form and the history of the generations, recorded ever 50 generations
final_population, record = nsga_util.run_nsga(ds, tsp_population, the_param)
print("\n")
I = sorted(final_population, key=lambda x :x[1])
for pop in I:
    print(pop[:2])
'''format of the population array'''
#0: time
#1: profit
#2: crowding distance
#3: rank
#4: path population
#5: packing population
#6: weights
print("Done")
