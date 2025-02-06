#! /usr/bin/env python3
########################################
# CS63: Artificial Intelligence, Lab 2
# Spring 2024, Swarthmore College
########################################

import TrafficJam
import FifteenPuzzle
from PriorityQueue import *
from Node import Node
from sys import argv

def main():
    if len(argv) < 2:
        print("Please provide a puzzle.")
        print("Usage: ./InformedSearch.py puzzle heuristic")
        exit()
    if len(argv) != 3:
        print("Please provide a heuristic.")
        print("Usage: ./InformedSearch.py puzzle heuristic")
        exit()
    try:
        heuristic = heuristics[argv[2]]
    except KeyError:
        print("unknown heuristic:", argv[2])
        print("options:", list(heuristics.keys()))
        exit()
    filename = argv[1]
    if "traffic" in filename:
        puzzle = TrafficJam.read_puzzle(filename)
    elif "fifteen" in filename:
        puzzle = FifteenPuzzle.read_puzzle(filename)
    agent = InformedSearchAgent(puzzle, heuristic)
    goalNode = agent.search()
    if goalNode is not None:
        path = agent.path_to(goalNode)
        print(path[0].state)
        for node in path[1:]:
            print(node.action)
            print(node.state)
        print("Path of length", len(path) - 1, "found")
    else:
        print("Could not solve puzzle:")
        print(puzzle)
    print("Expanded", agent.expanded, "nodes.")


def zeroHeuristic(state):
    return 0

heuristics = {"zero":      zeroHeuristic,
              "blocking":  TrafficJam.blockingHeuristic,
              "better":    TrafficJam.betterHeuristic,
              "displaced": FifteenPuzzle.displacedHeuristic,
              "manhattan": FifteenPuzzle.manhattanHeuristic,
              "bonus":     FifteenPuzzle.bonusHeuristic}

class InformedSearchAgent(object):
    def __init__(self, puzzle, heuristicFunction):
        """Stores the puzzle. Initializes an integer to count the number of
        nodes expanded by the search. Stores the heuristic function to be
        called during A* search."""
        self.initial_puzzle = puzzle
        self.expanded = 0
        self.heuristic = heuristicFunction

    def search(self):
        """This is the core method of this class. Implements A* search.

        Adds nodes to the priority queue with priority as the sum of
        the depth of the node and the heuristic function applied to
        the state of the node. Depth represents cost to get to this
        state and the heuristic function estimates the distance to the
        goal from this state.

        If a goal state is found, the corresponding node is returned.
        Otherwise, returns None.

        Increments expanded counter when a state's actions are taken."""
        node = Node(self.initial_puzzle, None, None, 0)
        pq = PriorityQueue()
        pq.insert(0, node)
        dic = dict()
        while not pq.isEmpty():
            currNode = pq.remove()
            if currNode.state.goalReached():
                return currNode
            if currNode.state not in dic:
                dic[currNode.state] = "visited"
                self.expanded += 1
                for move in currNode.state.getPossibleMoves():
                    nextState = currNode.state.nextState(move)
                    if nextState not in dic:
                        newNode = Node(nextState, currNode, move, currNode.depth + 1)
                        priority = newNode.depth + self.heuristic(newNode.state)
                        pq.insert(priority, newNode)
        return None

    
    def path_to(self, node):
        """Given a goal node, trace back through the parent pointers to
        return an ordered list of Nodes along a path from start to goal."""
        lst = []
        currNode = node
        lst.append(currNode)
        while currNode.parent is not None:
            lst.append(currNode.parent)
            currNode = currNode.parent
        lst.reverse()
        return lst


if __name__ == '__main__':
    main()
