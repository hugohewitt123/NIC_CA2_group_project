import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Dataset
import file_util as fu
import pack_util as pack
import path_util as path

#TODO re-write this:
def non_dom_sort(P):
    '''function to run the non-dominating sort'''
    #0: time
    #1: profit
    #2: crowding distance
    #3: rank
    #4: path population
    #5: packing population
    P1 = [P[0]]
    for p in P[1:]:
        P1.append(p)
        for q in P1:
            if p[0] < q[0] and p[1] > q[1]:
                #then p dominates
                P1.remove(q)
            elif p[0] > q[0] and p[1] < q[1]:
                #then p is dominated
                P1.remove(p)
                break
    return P1

def density_est(I):
    '''function to run the density estimation and crowding operator'''
    for i in range(2):
        I = sorted(I, key=lambda x :x[i])
        I[0][2] = I[len(I)-1][2] = float('inf')
        for j in range(len(I)-1):
            I[j][2] += (I[j+1][i]-I[j-1][i])
    return I


def crowded_comparison(p):
    '''function to comare population items'''
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
    for i in range(len(p)-1):
        while (p[i][3] < p[i+1][3]) or ((p[i][3] == p[i+1][3]) and (p[i][2] > p[i+1][2])):
            #p[i] < p[i+1] so swap them
            p[i+1], p[i] = p[i], p[i+1]
    return p


def make_new_pack_pop(population, profits, weights, tournament_size, knapsack_cap):
    '''function to run tournament selection, cross over and mutation for packing population'''
    new_pop = []
    while len(new_pop) < len(population):
        a, b = pack.tournament_selection(population, profits, weights, tournament_size, knapsack_cap)
        c, d = pack.single_point_crossover(a, b)
        e, f = pack.bitflip_mutation(c, d)
        new_pop.append(e)
        new_pop.append(f)
    return new_pop

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
    '''function to select paths for mutation'''
    N1 = []
    N2 = []
    visited1 = []
    visited2 = []
    for i in range(tournament_size):
        randchoice1 = random.choice([i for i in range(0,len(paths)) if i not in visited1])
        randchoice2 = random.choice([i for i in range(0,len(paths)) if i not in visited2])
        N1.append(randchoice1)
        N2.append(randchoice2)
        visited1.append(randchoice1)
        visited2.append(randchoice2)
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
    children = []
    for i in range(int(len(path_pop)/2)):
        a, b = path_tournament_selection(path_pop, path_dists, tournament_size)
        c, d = mutate_path(a, b)
        children.append(c)
        children.append(d)
    return children


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

def run_nsga(ds):
    '''function to run the nsga algorithm'''
    '''Parameters'''
    population_size = 50
    tournament_size = 10
    num_generations = 100
    #fill rate is the percentage of knapsack to fill to max capacity
    fill_rate            = 0.9
    '''problem constraints'''
    Vmin         = ds.min_speed
    Vmax         = ds.max_speed
    knapsack_cap = ds.knapsack_cap
    num_of_items = ds.num_of_items

    '''creating the packing population and initial children'''
    pack_pop = pack.generate_random_population(population_size, num_of_items, ds, knapsack_cap, fill_rate)
    '''creating the path population and evaluating distances'''
    path_pop, path_dists = generate_path_population(ds, population_size)

    for x in range(num_generations):
        '''creating the children for the paths and packs'''
        print("Generation : ", x+1)
        profits, weights = pack.get_profit_weights(pack_pop, ds)
        path_dists = []
        for i in path_pop:
            path_dists.append(path.get_path_dist(i))
        
        pack_children = make_new_pack_pop(pack_pop, profits, weights, tournament_size, knapsack_cap)
        pack_pop = pack_pop + pack_children

    ### TODO This is where 3-opt will go ### below is just temporary 
        path_children = generate_path_children(path_pop, path_dists, tournament_size)
        path_pop = path_pop + path_children
    ###

        times = evaluate_population(pack_pop, path_pop, ds, Vmax, Vmin, knapsack_cap)
        profits, weights = pack.get_profit_weights(pack_pop, ds)
        #for i in range(len(weights)):
        #    while weights[i] > knapsack_cap:
        #        for j in range(len(pack_pop[i])):
        #            if pack_pop[i][j] == 1:
        #                pack_pop[i][j] = 0
        #                break
        #        profits, weights = pack.get_profit_weights(pack_pop, ds)

        ## Start of the NSGA-II part ##
        #sorting the population into non-dominating ranks
        ranks = [-1] * len(times)
        distances = [0] * len(times)
        population = list(zip(profits, weights, distances, ranks, path_pop, pack_pop))
        for i in range(len(population)):
            population[i] = list(population[i])

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
        
        population = density_est(population)
        '''format for population list'''
        #0: time
        #1: profit
        #2: crowding distance
        #3: rank
        #4: path population
        #5: packing population
        #print(population)

        population = crowded_comparison(population)
        population = population[:len(population)//2]
        pack_pop = []
        path_pop = []
        for i in population:
            pack_pop.append(i[5])
            path_pop.append(i[4])
    for p in population:
        print(p[:4])

ds = fu.file_reader(0)
run_nsga(ds)