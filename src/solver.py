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
final_population, record, hvs = nu.run_nsga(ds, tsp_population, the_param)
print(f"elapsed_time is: {nu.time.time()-start_time}\n")

I = sorted(final_population, key=lambda x :x[1])
for pop in I:
    print(pop[:2])
print(hvs)
fu.write_results(I, hvs, the_param.exp_type)
'''format of the population array'''
#0: time
#1: profit
#2: crowding distance
#3: rank
#4: path population
#5: packing population
#6: weights
print("Done")

hvs_final = nu.calculate_hypervolume(final_population)
print(f"hvs recauculate: {hvs_final}")

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
plt.title('Blend Crossover')

# Add grid
plt.grid(True)

# Show legend
plt.legend()

# Show the plot in Visual Studio Code
plt.show()