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

def velocity(w, cap):
    '''funcition to work out the current velocity'''
    return 1.0 - ((1-0.1)/cap)*w

def tournament_selection(population, profits, weights, tournament_size, knapsack_cap):
    '''Function to select parents from the population'''
    N1 = []
    N2 = []
    visited1 = []
    visited2 = []
    #selecting a number random items from the population depending on the tournament size
    for i in range(tournament_size):
        randchoice1 = random.choice([i for i in range(0,len(population)) if i not in visited1])
        randchoice2 = random.choice([i for i in range(0,len(population)) if i not in visited2])
        N1.append(randchoice1)
        N2.append(randchoice2)
        visited1.append(randchoice1)
        visited2.append(randchoice2)
    #choosing the items in the tournament with the best profit
        #(given the knapsack capacity isn't violated)
    a = b = a_i = b_i = -1
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

def two_point_crossover(a, b):
    '''Function to perform two-point crossover on the knapsack'''
    x, y = sorted(random.sample(range(1, len(a)-1), 2))
    c = a[:x] + b[x:y] + a[y:]
    d = b[:x] + a[x:y] + b[y:]

    return c, d

def three_point_crossover(a, b):
    '''Function to perform three-point crossover on the knapsack'''
    x, y, z = sorted(random.sample(range(1, len(a)-1), 3))
    c = a[:x] + b[x:y] + a[y:z] + b[z:]
    d = b[:x] + a[x:y] + b[y:z] + a[z:]

    return c, d

def random_point_crossover(a, b):
    '''Function to perform random-point crossover on the knapsack'''
    num_points = random.randint(1, len(a)-1)
    points = sorted(random.sample(range(1, len(a)), num_points))
    
    c, d = a[:], b[:]
    switch = False
    for point in points:
        if switch:
            c[point:], d[point:] = d[point:], c[point:]
        switch = not switch

    return c, d

def binary_mask_crossover(a, b):
    mask = [random.choice([0, 1]) for _ in range(len(a))]
    c = [a[i] if mask[i] == 0 else b[i] for i in range(len(a))]
    d = [b[i] if mask[i] == 0 else a[i] for i in range(len(b))]
    return c, d

def blend_crossover(a, b, alpha=0.5):
    c = [a[i] if random.random() < alpha else b[i] for i in range(len(a))]
    d = [b[i] if random.random() < alpha else a[i] for i in range(len(b))]
    return c, d

def simulated_binary_crossover(a, b, eta=2, prob_cross=0.9):
    c = list(map(int, a))
    d = list(map(int, b))

    if random.random() < prob_cross:
        for i in range(len(a)):
            if random.random() < 0.5:
                beta = (2.0 * random.random())**(1.0 / (eta + 1))
                c[i] = int(0.5 * (((1 + beta) * a[i]) + (1 - beta) * b[i]))
                d[i] = int(0.5 * (((1 - beta) * a[i]) + (1 + beta) * b[i]))

    return c, d

def ordered_crossover(a, b):
    # Randomly select two crossover points
    points = sorted(random.sample(range(len(a)), 2))

    # Create masks to preserve selected segments
    mask_a = [False] * len(a)
    mask_b = [False] * len(b)

    # Mark selected segments in the masks
    for i in range(points[0], points[1]):
        mask_a[i] = True
        mask_b[i] = True

    # Get segments for offspring by copying the selected segments
    segment_a = [gene for gene, mask in zip(b, mask_a) if not mask]
    segment_b = [gene for gene, mask in zip(a, mask_b) if not mask]

    # Create offspring by combining segments and preserving order
    c = segment_a[:points[0]] + a[points[0]:points[1]] + segment_a[points[0]:]
    d = segment_b[:points[0]] + b[points[0]:points[1]] + segment_b[points[0]:]

    return c, d

def cycle_crossover(a, b):
    size = len(a)
    cycle = [False] * size
    child1, child2 = [-1] * size, [-1] * size

    # Start with the first cycle
    index = 0
    while not cycle[index]:
        cycle[index] = True

        child1[index] = a[index]
        child2[index] = b[index]

        value_b = b[index]
        index = a.index(value_b)

    # Fill in remaining elements
    for i in range(size):
        if not cycle[i]:
            child1[i] = b[i]
            child2[i] = a[i]

    return child1, child2

def displacement_crossover(a, b):
    # Randomly select a crossover segment
    segment_length = random.randint(1, min(len(a), len(b)) - 1)
    start_index = random.randint(0, min(len(a), len(b)) - segment_length)

    # Extract the selected segment from both parents
    segment_a = a[start_index:start_index + segment_length]
    segment_b = b[start_index:start_index + segment_length]

    # Create offspring by replacing the segment with the other parent's segment
    c = a[:start_index] + segment_b + a[start_index + segment_length:]
    d = b[:start_index] + segment_a + b[start_index + segment_length:]

    return c, d

def insertion_mutation(c, d):
    # Select a random element from chromosome 'c'
    element = random.choice(c)
    # Remove the selected element from chromosome 'c'
    c.remove(element)
    # Choose a random position in chromosome 'd' to insert the element
    insert_position = random.randint(0, len(d))
    d.insert(insert_position, element)

    # Select a random element from chromosome 'd'
    element = random.choice(d)
    # Remove the selected element from chromosome 'd'
    d.remove(element)
    # Choose a random position in chromosome 'd' to insert the element
    insert_position = random.randint(0, len(c))
    c.insert(insert_position, element)

    return c, d


def bitflip_mutation(c, d):
    '''function to perform bitflip mutation'''
    i = random.randint(0,len(c)-1)
    c[i] = ~c[i]+2
    i = random.randint(0,len(d)-1)
    d[i] = ~d[i]+2
    return c, d

def generate_random_population(population_size, num_of_items, ds, knapsack_cap,fill_rate):
    '''function to generate initial population'''
    population = []
    for i in range(population_size):
        lst = [0]*num_of_items
        weight = 0
        #filling the knapsack until the weight capacity is reached
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
        #if the pack plan picks up the item (1) get the weight and profit from the dataset
        if a[i] == 1:
            w += ds.items[i+1].weight
            p += ds.items[i+1].profit

    return p, w
def get_profit_weights(population, ds):
    '''function to get the total weight of the population'''
    profits = []
    weights = []
    #evaluates the weight and profit for the whole population
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
