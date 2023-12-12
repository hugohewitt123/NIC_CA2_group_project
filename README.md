# NIC_CA2_group_project
NIC group project to solve the travelling thief problem

<br/> Link to the GitHub problem page:
<br/> https://github.com/blankjul/gecco19-thief/tree/master

<h3>How to run: </h3>
Please run "solver.py" in folder "src"

<h3>Note that: </h3>
For dataset_idx: 0, 2, 3, 5 datasets, we just keep the original parameters unchanged and run as the step above; <br/>
For dataset_idx: 1, 4 datasets, we have to change the "exp_type: 20" to "exp_type: 0"; <br/>
For dataset_idx: 6, 8 datasets, we have to change the "run_local_tsp: True" to "run_local_tsp: False"; <br/>
For dataset_idx: 7 dataset, we have to change both the "run_local_tsp: True" to "run_local_tsp: False" and the "exp_type: 20" to "exp_type: 0". <br/>

<h3>How to plot: </h3>
Please run "plot.ipynb" in folder "src"


<h3> Params: </h3>
Change the param in resource/param_properties <br/> 
name (Type): Description <br/> 
population_size_nsg (int): Population size <br/> 
evaluations_tsp (int): Rounds of fitness in TSP <br/> 
run_local_tsp (bool): Optimise every node in TSP <br/> 
tournament_size_ksp (int): Tournament size for fitness test in KSP <br/> 
num_generations_ksp (int): Rounds of fitness in KSP <br/> 
fill_rate_ksp (float): Percentage of the knapsack to fill <br/> 
random_seed (int): Vaule used to ensure the reproducible sequence of random numbers produced <br/> 
exp_type (int): Number used to define different experiments based on different combination of crossover and mutation operators <br/> 
dataset_idx (int): Which file reading <br/> 

<h3> File Index (dataset_idx): </h3>
0: a280-n279.txt <br/>
1: a280-n1395.txt <br/>
2: a280-n2790.txt <br/>
3: fnl4461-n4460.txt <br/>
4: fnl4461-n22300.txt <br/>
5: fnl4461-n44600.txt <br/>
6: pla33810-n33809.txt <br/>
7: pla33810-n169045.txt <br/>
8: pla33810-n338090.txt <br/>

<h3> exp_type Meaning Indicator: </h3>
0:  single_point_crossover     + bitflip_mutation <br/> 
1:  single_point_crossover     + inversion_mutation <br/> 
2:  single_point_crossover     + gaussian_mutation <br/> 
3:  two_point_crossover        + bitflip_mutation <br/> 
4:  three_point_crossover      + bitflip_mutation <br/> 
5:  random_point_crossover     + bitflip_mutation <br/> 
6:  binary_mask_crossover      + bitflip_mutation <br/> 
7:  simulated_binary_crossover + bitflip_mutation <br/> 
8:  blend_crossover            + bitflip_mutation <br/> 
9:  uniform_crossover          + bitflip_mutation <br/> 
10: ordered_crossover          + bitflip_mutation <br/> 
11: cycle_crossover            + bitflip_mutation <br/> 
12: displacement_crossover     + bitflip_mutation <br/> 
other number: ordered_crossover + inversion_mutation (our best choice and result)<br/> 
