########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2024, Swarthmore College
########################################
# NOTE: These functions should use good modularity!  In particular, they should
#       contain minimal code replication; the parts of the algorithms that
#       overlap should be extracted into functions that can be called from 
#       both places.
########################################

from math import exp
from numpy.random import choice, multinomial 


def beam_search(problem, pop_size, steps, max_neighbors):
    """Implementes the beam search local search algorithm.
    inputs:
        - problem: A TSP instance.
        - pop_size: Number of candidates tracked.
        - steps: Number of moves moves to make in a given run.
        - max_neighbors: Number of neighbors generated each round for each
                candidate in the population.
    returns: best_candidate, best_cost
        The best candidate identified by the search and its cost.

    NOTE: In this case, you should always call random_neighbor(), rather
          than best_neighbor().
    """
    print("BS: ")
    candidate = problem.random_candidate()
    cost = problem.cost(candidate)
    best_candidate = candidate
    best_cost = cost
    pops = []
    for i in range(pop_size):
        pops.append(problem.random_candidate())
    # pop.append(problem.random_candidate() for i in range(pop_size))
    for j in range(steps):
        best_neigh_cost = problem.cost(candidate)
        best_neigh = candidate
        costs = []
        neighbors = []
        for pop in pops:
            for k in range(max_neighbors):
                curr_neighbor, curr_cost = problem.random_neighbor(pop)
                costs.append(curr_cost)
                neighbors.append(curr_neighbor)
        costs, neighbors = zip(*sorted(zip(costs, neighbors)))
        best_neigh_cost = costs[0]
        best_neigh = neighbors[0]
        pops = neighbors[:pop_size]
        if best_neigh_cost < best_cost:
            best_cost = best_neigh_cost
            best_candidate = best_neigh
            print("New best cost is: %f" % (best_cost))
    return best_candidate, best_cost
        


def stochastic_beam_search(problem, pop_size, steps, init_temp,
                           temp_decay, max_neighbors):
    """Implementes the stochastic beam search local search algorithm.
    Inputs:
        - problem: A TSP instance.
        - pop_size: Number of candidates tracked.
        - steps: The number of moves to make in a given run.
        - init_temp: Initial temperature. Note that temperature has a
                slightly different interpretation here than in simulated
                annealing.
        - temp_decay: Multiplicative factor by which temperature is reduced
                on each step. Temperature parameters should be chosen such
                that e^(-cost / temp) never reaches 0.
        - max_neighbors: Number of neighbors generated each round for each
                candidate in the population.
    Returns: best_candidate, best_cost
        The best candidate identified by the search and its cost.

    NOTES: In this case, you should always call random_neighbor(), rather
          than best_neighbor().
    """
    print("SBS:")
    candidate = problem.random_candidate()
    cost = problem.cost(candidate)
    best_candidate = candidate
    best_cost = cost
    pops = []
    for i in range(pop_size):
        pops.append(problem.random_candidate())
    temp = init_temp
    for j in range(steps):
        best_neigh_cost = problem.cost(candidate)
        best_neigh = candidate
        costs = []
        neighbors = []
        for pop in pops:
            for k in range(max_neighbors):
                curr_cost = problem.random_neighbor(pop)[1]
                curr_neighbor = problem.random_neighbor(pop)[0]
                costs.append(curr_cost)
                neighbors.append(curr_neighbor)
                if curr_cost < best_neigh_cost:
                    best_neigh_cost = curr_cost
                    best_neigh = curr_neighbor
        if best_neigh_cost < best_cost:
            best_cost = best_neigh_cost
            best_candidate = best_neigh
            print("New best cost is: %f" % (best_cost))
        try:
            pops = prob(problem, temp, neighbors, pop_size)
        except:
            return best_candidate, best_cost
        temp *= temp_decay

    return best_candidate, best_cost


def prob(problem, temp, neighbors, pop_size):
    indices = list(range(len(neighbors)))
    probs = [exp(problem.cost(nei) * (-1) / temp) for nei in neighbors]
    summ = sum(probs)
    probs2 = []
    for prob in probs:
        probs2.append(prob/summ)
    choices = choice(indices, pop_size, p=probs2)
    neis = []
    for c in choices:
        neis.append(neighbors[c])
    return neis
