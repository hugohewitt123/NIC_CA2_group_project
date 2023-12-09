import math
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import Dataset
import file_util as fu

'''Goal is to minimize time and maximize profit'''

def node_dist(node1, node2):
    '''Function to calculate the euclidean distance'''
    z = pow((node1.coord_x - node2.coord_x),2) + pow((node1.coord_y - node2.coord_y),2)
    z = math.sqrt(z)
    return(z)

def check_problem_constraints(knapsack_capacity):
    '''function to check that the problem constraints aren't violated'''
    ###TODO###

def velocity(w, cap):
    '''funcition to work out the current velocity'''
    return 1.0 - ((1-0.1)/cap)*w

def tournament_selection(population, profits, weights, tournament_size, knapsack_cap):
    '''Function to select parents from the population'''
    N1 = []
    N2 = []
    visited1 = []
    visited2 = []
    for i in range(tournament_size):
        randchoice1 = random.choice([i for i in range(0,len(population)) if i not in visited1])
        randchoice2 = random.choice([i for i in range(0,len(population)) if i not in visited2])
        N1.append(randchoice1)
        N2.append(randchoice2)
        visited1.append(randchoice1)
        visited2.append(randchoice2)
    a = b = a_i = b_i = 0
    for i in N1:
        if profits[i] > a and weights[i] < knapsack_cap:
            a = profits[i]
            a_i = i
    for i in N2:
        if profits[i] < b and weights[i] < knapsack_cap:
            b = profits[i]
            b_i = i
    return population[a_i], population[b_i]


def single_point_crossover(a, b):
    '''funciton to perform single point crossover on the knapsack'''
    x = random.randint(1, len(a)-1)
    c = a[:x] + b[x:]
    d = b[:x] + a[x:]

    return c, d

def bitflip_mutation(c, d):
    '''function to perform bitflip mutation'''
    i = random.randint(0,len(c))
    c[i] = ~c[i]+2
    i = random.randint(0,len(d))
    d[i] = ~d[i]+2
    return c, d

def generate_random_population(population_size, num_of_items, ds, knapsack_cap,fill_rate):
    '''function to generate initial population'''
    population = []
    for i in range(population_size):
        lst = [0]*num_of_items
        weight = 0
        while weight < knapsack_cap*fill_rate:
            rnd = random.randint(0,num_of_items-1)
            if lst[rnd] == 0:
                lst[rnd] = 1
                weight += ds.items[rnd+1].weight
        population.append(lst)
    return population

def evaluate_pack(a, ds):
    '''function to return the weight and proffit of a packing plan'''
    p = 0
    w = 0
    for i in range(len(a)):
        if a[i] == 1:
            w += ds.items[i+1].weight
            p += ds.items[i+1].profit

    return p, w
def get_profit_weights(population, ds):
    '''function to get the total weight of the population'''
    profits = []
    weights = []
    for pop in population:
        p = 0
        w = 0
        for i in range(len(pop)):
            if pop[i] == 1:
                w += ds.items[i+1].weight
                p += ds.items[i+1].profit
        weights.append(w)
        profits.append(p)
    return profits, weights

def knapsac(ds):
    '''
    function to do bi-objective optimisation of the knapsac problem
    In order to maximise profit 
    '''
    p_city_route   = []
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

    '''Generate initial packing plan population'''
    population = generate_random_population(population_size, num_of_items, ds, knapsack_cap, fill_rate)
    #print(population)
    '''evaluate the population'''
    profits, weights = get_profit_weights(population, ds)

    '''First stage of the EA'''
    a, b = tournament_selection(population, profits, weights, tournament_size, knapsack_cap)
    #print(a)
    #print(b)
    profita, weighta = evaluate_pack(a,ds)
    profitb, weightb = evaluate_pack(b,ds)
    print("p(a) = ",profita," w(a) = ",weighta)
    print("p(b) = ",profitb," w(b) = ",weightb)

    c, d = single_point_crossover(a, b)
    #print(c)
    #print(d)
    #profitc, weightc = evaluate_pack(c,ds)
    #profitd, weightd = evaluate_pack(d,ds)

    e, f = bitflip_mutation(c, d)
    #print(e)
    #print(f)
    profite, weighte = evaluate_pack(e,ds)
    profitf, weightf = evaluate_pack(f,ds)
    print("p(e) = ",profite," w(e) = ",weighte)
    print("p(f) = ",profitf," w(f) = ",weightf)

    #print(weights)
    #print(profits)
    #print(population)
    
    #v = v(weight, knapsack_cap) #for velocity at a given point
    #t = d/v #for working out the time between nodes

#Some testing
#ds = fu.file_reader(0)
#knapsac(ds)
