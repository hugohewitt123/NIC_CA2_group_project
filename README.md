# NIC_CA2_group_project
NIC group project to solve the travelling thief problem

<br/> Link to the GitHub problem page:
<br/> https://github.com/blankjul/gecco19-thief/tree/master

<h3>How to run: </h3>
Please run "solver.py" in folder "src"


<h3> Params: </h3>
Change the param in resource/param_properties <br/> 
name (Type): Description <br/> 
population_size_nsg (int): Population size <br/> 
evaluations_tsp (int): Rounds of fitness in TSP <br/> 
run_local_tsp (bool): Optimise every node in TSP <br/> 
tournament_size_ksp (int): Tournament size for fitness test in KSP <br/> 
num_generations_ksp (int): Rounds of fitness in KSP <br/> 
fill_rate_ksp (float): Percentage of the knapsack to fill <br/> random_seed (int): Vaule used to ensure the reproducible sequence of random numbers produced
<br/> exp_type (int): Number used to define different experiments based on different combination of crossover and mutation functions
<br/> 
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
3:  single_point_crossover     + inserted_mutation <br/> 
4:  two_point_crossover        + bitflip_mutation <br/> 
5:  three_point_crossover      + bitflip_mutation <br/> 
6:  random_point_crossover     + bitflip_mutation <br/> 
7:  binary_mask_crossover      + bitflip_mutation <br/> 
8:  simulated_binary_crossover + bitflip_mutation <br/> 
9:  blend_crossover            + bitflip_mutation <br/> 
10: uniform_crossover          + bitflip_mutation <br/> 
11: ordered_crossover          + bitflip_mutation <br/> 
11: cycle_crossover            + bitflip_mutation <br/> 
12: displacement_crossover     + bitflip_mutation <br/> 
