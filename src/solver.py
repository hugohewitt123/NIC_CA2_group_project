import Params
import tsp_algo
import file_util as fu
import TSP_Data
import nsga_util as nu
start_time = nu.time.time()
# The main program
the_param: Params = fu.read_param_properties()
nu.random.seed(the_param.random_seed)
tsp_graph_data = TSP_Data.TSP_Data()
tsp_population, tsp_graph_data = tsp_algo.tsp_solve(the_param.dataset_idx, the_param)
ds = fu.file_reader(the_param.dataset_idx)
#returns the final population form and the history of the generations, recorded ever 50 generations
final_population, record = nu.run_nsga(ds, tsp_population, the_param)
print(f"elapsed_time is: {nu.time.time()-start_time}\n")

pf = nu.np.array([pop[:2] for pop in sorted(final_population, key=lambda x :x[1])])
print(pf)
'''format of the population array'''
#0: time
#1: profit
#2: crowding distance
#3: rank
#4: path population
#5: packing population
#6: weights
print("Done")

import matplotlib.pyplot as plt
# Extract x and y values
x_values = [individual[0] for individual in I]
y_values = [individual[1] for individual in I]

# Create scatter plot
plt.scatter(x_values, y_values, marker='o', label='Population')

# Set axis labels
plt.xlabel('Time')
plt.ylabel('Value')

# Set plot title
plt.title('Simulated Binary Crossover')

# Add grid
plt.grid(True)

# Show legend
plt.legend()

# Show the plot in Visual Studio Code
plt.show()
min_pf = nu.np.min(pf, axis=0)
max_pf = nu.np.max(pf, axis=0)
normalized_pf = (pf - min_pf) / (max_pf - min_pf)
hv = nu.Hypervolume(nu.np.array([1.0, 1.0]))
hypervolume_value = hv.do(normalized_pf)
print("Hypervolume:", hypervolume_value)
