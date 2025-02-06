########################################
# CS63: Artificial Intelligence, Lab 3
# Spring 2024, Swarthmore College
########################################

from random import random

def hill_climbing(problem, runs, steps, rand_move_prob):
    """Implementes the hill climbing local search algorithm.
    Inputs:
        - problem: A TSP instance.
        - runs: Number of times to start from a random initial candidate.
        - steps: Number of moves to make in a given run.
        - rand_move_prob: prob of a random neighbor on any given step.
    Returns: best_candidate, best_cost
        The best candidate identified by the search and its cost.

    NOTE: When doing a random move use random_neighbor(), otherwise use
        best_neighbor(). 
    """
    print("HC: ")
    candidate = problem.random_candidate()
    cost = problem.cost(candidate)
    best_candidate = candidate
    best_cost = cost
    for i in range(runs):
        print("Starting run " + str(i))
        curr_candidate = problem.random_candidate()
        curr_cost = problem.cost(curr_candidate)
        for j in range(steps):
            r = random()
            if r < rand_move_prob:
                curr_candidate, curr_cost = problem.random_neighbor(curr_candidate)
            else:
                neighbor_candidate, neighbor_cost = problem.best_neighbor(curr_candidate)
                if neighbor_cost < curr_cost:
                    curr_cost = neighbor_cost
                    curr_candidate = neighbor_candidate
            if curr_cost < best_cost:
                best_candidate = curr_candidate
                best_cost = curr_cost
                print("New best cost is: %f" % (best_cost))

    return best_candidate, best_cost
