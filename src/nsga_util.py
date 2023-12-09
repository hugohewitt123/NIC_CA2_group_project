import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Dataset
import file_util as fu
import pack_util as pack
import path_util as path


def non_dom_sort(Rt):
    '''function to run the non-dominating sort'''

def density_est():
    '''function to run the density estimation and crowding operator'''

def crowded_comparison(i_ranks, i_distances, j_ranks, j_distances):
    '''function to comare population items'''
    #1. Non-domination rank (irank)
    #2. Local crowding distance (idistance)
    #We now define a partial order <_n as :
    #i <_n j if(i_rank < j_rank) or 
    #           ((i_rank = j_rank) and (i_distance > j_distance))

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
            if path_pop[n][i] in nodes:
                w += weights[nodes.index(node)]
                v = Vmax - ((Vmax-Vmin)/cap)*w
                d = path.cal_dist(path_pop[n][i], path_pop[n][i+1])
                t += d/v
            else:
                d = path.cal_dist(path_pop[n][i], path_pop[n][i+1])
                t += d/v
        time_list.append(t)
    return(time_list)


def run_nsga(ds):
    '''function to run the nsga algorithm'''
    '''Parameters'''
    population_size      = 50
    tournament_size      = 10
    termination_criteria = 10000
    #fill rate is the percentage of knapsack to fill to max capacity
    fill_rate            = 0.9
    '''problem constraints'''
    Vmin         = ds.min_speed
    Vmax         = ds.max_speed
    knapsack_cap = ds.knapsack_cap
    num_of_items = ds.num_of_items

    '''creating the packing population and initial children'''
    pack_pop = pack.generate_random_population(population_size, num_of_items, ds, knapsack_cap, fill_rate)
    '''evaluate the random pack population'''
    profits, weights = pack.get_profit_weights(pack_pop, ds)
    #generating the children
    pack_children = make_new_pack_pop(pack_pop, profits, weights, tournament_size, knapsack_cap)

    '''creating the path population and evaluating distances'''
    path_pop, path_dists = generate_path_population(ds, population_size)

    times = evaluate_population(pack_pop, path_pop, ds, Vmax, Vmin, knapsack_cap)

    ## Start of the NSGA-II part ##
    Rt = pack_pop + pack_children
    Rt_profits, Rt_weights = pack.get_profit_weights(Rt, ds)
    #f = non_dom_sort(Rt, Rt_profits)

ds = fu.file_reader(0)
run_nsga(ds)