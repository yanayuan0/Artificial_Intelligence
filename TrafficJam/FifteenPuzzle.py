#! /usr/bin/env python3
########################################
# CS63: Artificial Intelligence, Lab 2
# Spring 2024, Swarthmore College
########################################

import numpy as np
import random
import json
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="File to read for puzzle.")
    args = parser.parse_args()
    puzzle = read_puzzle(args.file)
    playGame(puzzle)

def displacedHeuristic(state):
    """Finds the number of pieces that are out of place in the given
    FifteenPuzzlqe state."""
    num = 1
    counter = 0
    for row in state.board:
        for item in row:
            if item != num:
                counter +=1
            num +=1
    counter -= 1
    return counter
               

def manhattanHeuristic(state):
    """Sums up each piece's distance (in horizonal/vertical moves) from
    its goal position in the given FifteenPuzzle state."""
    counter = 0
    rowlen = len(state.board[0])
    for i in range(0, rowlen):
        for j in range(0, rowlen):
            item = state.board[i][j]
            x = item % rowlen -1
            if (item % rowlen == 0):
                x = rowlen - 1
            y = (item -x-1)/rowlen
            if (item != 0):
                counter += abs(x -j) + abs(y-i)    
    return int(counter)



def bonusHeuristic(state):
    """(optional) A better heuristic than the Manhattan distance.

    This heuristic should be better in that:
    - It never estimates fewer moves than manhattanHeuristic.
    - It sometimes estimates more moves than manhattanHeuristic.
    - It never estimates more moves than are required (it's admissible).

    Update this comment to describe your heuristic."""
    raise NotImplementedError("OPTIONAL")


class FifteenPuzzle:
    """Implements a generalized fifteen puzzle (n^2 - 1 puzzle).  The
    board represents the numbered sliding tiles of sliding tile
    puzzle.  The zero on the board indicates a blank space; adjacent
    tiles can slide into the blank space. The goal of the game is to
    arrange the tiles numbered 1 ... n^2-1 in inreasing order from the
    top-left.

    """
    def __init__(self, size=None, board=None, empty_cell=None, goal=None):
        """Initializes the board. If empty_cell or goal are provided they
        will be stored. Otherwise, they will be computed.
        """
        assert (size is not None) or (board is not None), \
                "must specify either size or board"
        if board is None:
            self.board = np.arange(size*size).reshape([size,size]) + 1
            self.board[-1,-1] = 0
        else:
            self.board = board.copy()
        if empty_cell is None:
            r,c = np.where(self.board == 0)
            self.empty_cell = (r[0], c[0])
        else:
            self.empty_cell = empty_cell
        if goal is not None:
            self.goal = goal
        else:
            self.goal = np.arange(size*size).reshape([size,size]) + 1
            self.goal[-1,-1] = 0
        self._str = None

    def __repr__(self):
        if self._str is None:
            s = "\n".join("\t".join(map(str, row)) for row in self.board)
            self._str = s.expandtabs(3)
        return self._str

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        try:
            return np.array_equal(self.board, other.board)
        except AttributeError:
            return False

    def goalReached(self):
        """Compares the current board to the goal."""
        return np.array_equal(self.board, self.goal)

    def getPossibleMoves(self):
        """Returns a subset of [U,D,L,R] indicating the feasible directions
        that the BLANK SPACE could move."""
        moves = []
        if self.empty_cell[0] > 0:
            moves.append("U")
        if self.empty_cell[0] < self.board.shape[0] - 1:
            moves.append("D")
        if self.empty_cell[1] > 0:
            moves.append("L")
        if self.empty_cell[1] < self.board.shape[1] - 1:
            moves.append("R")
        return moves

    def nextState(self, move):
        """Create a new game with the board updated according to the
        move."""
        nextBoard = FifteenPuzzle(None, self.board, self.empty_cell, self.goal)
        row,col = self.empty_cell
        if move == "U":
            nextBoard.board[row,col] = nextBoard.board[row-1,col]
            nextBoard.board[row-1,col] = 0
            nextBoard.empty_cell = (row-1,col)
        elif move == "D":
            nextBoard.board[row,col] = nextBoard.board[row+1,col]
            nextBoard.board[row+1,col] = 0
            nextBoard.empty_cell = (row+1,col)
        elif move == "L":
            nextBoard.board[row,col] = nextBoard.board[row,col-1]
            nextBoard.board[row,col-1] = 0
            nextBoard.empty_cell = (row,col-1)
        elif move == "R":
            nextBoard.board[row,col] = nextBoard.board[row,col+1]
            nextBoard.board[row,col+1] = 0
            nextBoard.empty_cell = (row,col+1)
        return nextBoard


def generate_puzzle(size=4, moves=1000, seed=None):
    """Generates a solvable puzzle by starting from the goal state and
    shuffling for some number of random moves."""
    puzzle = FifteenPuzzle(size)
    random.seed(seed)
    for _ in range(moves):
        puzzle = puzzle.nextState(random.choice(puzzle.getPossibleMoves()))
    return puzzle


def read_puzzle(filename):
    """Reads setting from a file and calls generatePuzzle."""
    with open(filename) as f:
        puzzle_args = json.load(f)
    return generate_puzzle(**puzzle_args)


def playGame(puzzle):
    """Allows a human user to play a game."""
    steps = 0
    while not puzzle.goalReached():
        print(puzzle)
        #print(puzzle.board)
        moves = puzzle.getPossibleMoves()
        print("moves:", ", ".join(moves))
        choice = input("Select move (or q to quit): ")
        if choice == 'q':
            return
        if choice not in moves:
            print("invalid move")
            continue
        puzzle = puzzle.nextState(choice)
        steps += 1
    print(puzzle)
    print("You solved the puzzle in %d moves" % (steps))

if __name__ == '__main__':
    main()
