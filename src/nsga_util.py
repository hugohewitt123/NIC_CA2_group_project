import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Dataset
from functools import cmp_to_key
import file_util as fu
import pack_util as pack
import path_util as path
import Params

def non_dom_sort(P):
    '''function to run the non-dominating sort'''
    P1 = [P[0]]
    #start at the 2nd element so not to compare the initial one with itself
    for p in P[1:]:
        P1.append(p)
        for q in P1:
            if p[0] < q[0] and p[1] > q[1]:
                #then p dominates so q is removed
                P1.remove(q)
            elif p[0] > q[0] and p[1] < q[1]:
                #then p is dominated so p is removed
                P1.remove(p)
                break
    return P1

def density_est(I):
    '''function to run the density estimation and crowding operator'''
    for i in range(2):
        I = sorted(I, key=lambda x :x[i])
        I[0][2] = I[len(I)-1][2] = float('inf')
        for j in range(len(I)-1):
            I[j][2] = I[j][2] + (I[j+1][i]-I[j-1][i])
    return I

def compare(i, j):
    '''function to compare population items'''
    #1. Non-domination rank (i_rank)
    #2. Local crowding distance (i_distance)
    #We now define a partial order <_n as :
    #i <_n j if(i_rank < j_rank) or 
    #           ((i_rank = j_rank) and (i_distance > j_distance))
    '''format for population list (p)'''
        #0: time
        #1: profit
        #2: crowding distance
        #3: rank
        #4: path population
        #5: packing population
        #6: weights
    #compare the items with each other and use the formula from the paper to decide which one is better
    if (i[3] < j[3]) or ((i[3] == j[3]) and (i[2] > j[2])):
        #i < j
        return -1
    elif (i[3] > j[3]) or ((i[3] == j[3]) and (i[2] < j[2])):
        #i > j
        return 1
    else:
        #i = j
        return 0

def make_new_pack_pop(population, profits, weights, tournament_size, knapsack_cap, ds):
    '''function to run tournament selection, cross over and mutation for packing population'''
    new_pop = []
    while len(new_pop) < len(population):
        a, b = pack.tournament_selection(population, profits, weights, tournament_size, knapsack_cap)
        c, d = pack.single_point_crossover(a, b)
        # c, d = pack.two_point_crossover(a, b)
        # c, d = pack.three_point_crossover(a, b)
        # c, d = pack.random_point_crossover(a, b)
        # c, d = pack.binary_mask_crossover(a, b)
        # c, d = pack.simulated_binary_crossover(a, b)
        # c, d = pack.blend_crossover(a, b)
        
        # Priyanka's code
        # c, d = pack.ordered_crossover(a,b)
        # c, d = pack.cycle_crossover(a,b)
        # c, d = pack.displacement_crossover(a, b)
        
        #mutation
        #e, f = pack.insertion_mutation(c, d)
        e, f = pack.bitflip_mutation(c, d)
        
        pe, we = pack.evaluate_pack(e, ds)
        pf, wf = pack.evaluate_pack(f, ds)
        #for ensuring the weight of the new child knapsack is not exceeded
        if we <= knapsack_cap and wf <= knapsack_cap:
            new_pop.append(e)
            new_pop.append(f)
    return new_pop

#not used now 3-opt works
def generate_path_population(ds, population_size):
    '''function to generate the path population'''
    path_pop = []
    path_dists = []
    for i in range(population_size):
        init_path = path.get_random_path(ds)
        path_pop.append(init_path)
        path_dists.append(path.get_path_dist(init_path))
    return path_pop, path_dists

def evaluate_population(pack_pop, path_pop, ds, Vmax, Vmin, cap):
    '''function to work out the time for the population given weights'''
    time_list = []
    #collect the weights for the items being picked up at each node
    for n in range(len(pack_pop)):
        nodes  = []
        weights = []
        for i in range(len(pack_pop[n])):
            if pack_pop[n][i] == 1:
                nodes.append(ds.items[i+1].assigned_node)
                weights.append(ds.items[i+1].weight)
        w = 0
        t = 0
        v = Vmax
        #run over each node in the path, calculate the distance and if an item is picked up
        #then calculate the time based on the distance and velocity(that is dependent onthe weight)
        for i in range(len(path_pop[n])-1):
            if path_pop[n][i].node_id in nodes:
                w += weights[nodes.index(path_pop[n][i].node_id)]
                if w < cap:
                    v = Vmax - ((Vmax-Vmin)/cap)*w
                else:
                    v = Vmin
                d = path.cal_dist(path_pop[n][i], path_pop[n][i+1])
                t += d/v
            else:
                d = path.cal_dist(path_pop[n][i], path_pop[n][i+1])
                t += d/v
        time_list.append(t)
    return(time_list)

def path_tournament_selection(paths, path_dists, tournament_size):
    '''function to select paths'''
    N1 = []
    N2 = []
    visited1 = []
    visited2 = []
    #randomly select paths in the population
    for i in range(tournament_size):
        randchoice1 = random.choice([i for i in range(0,len(paths)) if i not in visited1])
        randchoice2 = random.choice([i for i in range(0,len(paths)) if i not in visited2])
        N1.append(randchoice1)
        N2.append(randchoice2)
        visited1.append(randchoice1)
        visited2.append(randchoice2)
    #choose the paths with the best distance (as a smaller distance means less time to travel)
    a = b = a_i = b_i = 0
    for i in N1:
        if path_dists[i] > a:
            a = path_dists[i]
            a_i = i
    for i in N2:
        if path_dists[i] < b:
            b = path_dists[i]
            b_i = i
    return paths[a_i], paths[b_i]

def generate_path_children(path_pop, path_dists, tournament_size):
    '''function to generate the path children'''
    #this function doubles the path population as specified in the NSGA requirements
    children = []
    for i in range(int(len(path_pop)/2)):
        a, b = path_tournament_selection(path_pop, path_dists, tournament_size)
        #c, d = mutate_path(a, b)
        children.append(a)
        children.append(b)
    return children

#temporary replacement for 3-opt this function is deprecieated
def mutate_path(c, d):
    '''funciton to mutate the paths'''
    visited = []
    randchoicea = []
    for i in range(2):
        randchoicea.append(random.choice([i for i in range(1,len(c)) if i not in visited]))
        visited.append(randchoicea[i])
    visited = []
    randchoiceb = []
    for i in range(2):
        randchoiceb.append(random.choice([i for i in range(1,len(d)) if i not in visited]))
        visited.append(randchoiceb[i])
    c[randchoicea[0]:randchoicea[1]] = c[randchoicea[0]:randchoicea[1]][::-1]
    d[randchoiceb[0]:randchoiceb[1]] = d[randchoiceb[0]:randchoiceb[1]][::-1]
    return c, d

def run_nsga(ds, path_population, the_param):
    '''function to run the nsga algorithm'''
    '''Parameters'''
    population_size = the_param.population_size_nsg
    tournament_size = the_param.tournament_size_ksp
    num_generations = the_param.num_generations_ksp
    #fill rate is the percentage of knapsack to fill to max capacity
    fill_rate       = the_param.fill_rate_ksp
    '''problem constraints'''
    Vmin         = ds.min_speed
    Vmax         = ds.max_speed
    knapsack_cap = ds.knapsack_cap
    num_of_items = ds.num_of_items

    #creating the packing population and initial children
    pack_pop = pack.generate_random_population(population_size, num_of_items, ds, knapsack_cap, fill_rate)
    #creating the path population and evaluating distances
    path_pop = path_population #The depreiceiated code: generate_path_population(ds, population_size)
    path_dists = []
    #evaluate the distances of the population
    for i in path_pop:
        path_dists.append(path.get_path_dist(i))
    record = []
    #loop for the generations of the NSGA algorithm
    for x in range(num_generations):
        print("Generation : ", x+1, end='\r')
        profits, weights = pack.get_profit_weights(pack_pop, ds)
        path_dists = []
        for i in path_pop:
            path_dists.append(path.get_path_dist(i))
        #generate the packing plan children
        pack_children = make_new_pack_pop(pack_pop, profits, weights, tournament_size, knapsack_cap, ds)
        pack_pop = pack_pop + pack_children
        #generate the path children
        path_children = generate_path_children(path_pop, path_dists, tournament_size)
        path_pop = path_pop + path_children

        #evaluate the new population for time, weight and profit
        times = evaluate_population(pack_pop, path_pop, ds, Vmax, Vmin, knapsack_cap)
        profits, weights = pack.get_profit_weights(pack_pop, ds)

        #zipping the populations together with their associated rank, profitsm weights etc
        ranks = [-1] * len(times)
        distances = [0] * len(times)
        population = list(zip(times, profits, distances, ranks, path_pop, pack_pop, weights))
        for i in range(len(population)):
            population[i] = list(population[i])
        '''format for population list'''
            #0: time
            #1: profit
            #2: crowding distance
            #3: rank
            #4: path population
            #5: packing population
            #6: weights
        
        ## Start of the NSGA-II part ##
        #sorting the population into non-dominating ranks
        rankiter = 0
        P0 = list(population)
        done = 0
        while done < len(times):
            P1 = non_dom_sort(P0)
            for p in P1:
                done+=1
                P0.remove(p)
                population[population.index(p)][3] = rankiter
            rankiter += 1
        
        #working out the crowding distance on the population
        population = density_est(population)

        #srting the population according to the crowding distance and non-domination rank
        population = sorted(population, key=cmp_to_key(compare), reverse=False)
        
        #cutting the population in half so that the best half 
        # is put forward to the next generation
        population = population[:len(population)//2]
        pack_pop = []
        path_pop = []
        for i in population:
            pack_pop.append(i[5])
            path_pop.append(i[4])
        #keeping a record of the population ever 50 generations
        if x % 50:
            record.append(population)
    return population, record
    #print("\n")
    #for p in population:
    #    print(p[:2])

#ds = fu.file_reader(0)
#run_nsga(ds)