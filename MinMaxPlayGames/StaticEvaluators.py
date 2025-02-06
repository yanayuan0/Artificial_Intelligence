########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2024, Swarthmore College
########################################

import numpy as np
from random import choice
from Mancala import Mancala
from Breakthrough import Breakthrough

def nimBasicEval(nim_game):
    """returns +1 or -1 on win/loss, else returns 0
    This is basically a 'dummy' eval function, it will run,
    but it won't do anything useful if you can't expand the 
    whole tree (but with Nim, the branching factor is only 3,
    so that's probably ok)
    """
    if nim_game.isTerminal:
        return nim_game.winner
    else:
        return 0

def mancalaBasicEval(mancala_game):
    """Difference between the scores for each player.
    Returns +9999 if player +1 has won.
    Returns -9999 if player -1 has won.

    Otherwise returns (player +1's score) - (player -1's score).

    Remember that the number of houses and seeds may vary."""
    if mancala_game.isTerminal:
        if mancala_game.winner == 1:
            return +9999
        elif mancala_game.winner == -1:
            return -9999
        else:
            return 0
    else:
        return mancala_game.scores[0] - mancala_game.scores[1]

def breakthroughBasicEval(breakthrough_game):
    """Measures how far each player's pieces have advanced
    and returns the difference.

    Returns +9999 if player +1 has won.
    Returns -9999 if player -1 has won.

    Otherwise finds the rank of each piece (number of rows onto the board it
    has advanced), sums these ranks for each player, and
    returns (player +1's sum of ranks) - (player -1's sum of ranks).

    An example on a 5x3 board:
    ------------
    |  0  1  1 |  <-- player +1 has two pieces on rank 1
    |  1 -1  1 |  <-- +1 has two pieces on rank 2; -1 has one piece on rank 4
    |  0  1 -1 |  <-- +1 has (1 piece * rank 3); -1 has (1 piece * rank 3)
    | -1  0  0 |  <-- -1 has (1*2)
    | -1 -1 -1 |  <-- -1 has (3*1)
    ------------
    sum of +1's piece ranks = 1 + 1 + 2 + 2 + 3 = 9
    sum of -1's piece ranks = 1 + 1 + 1 + 2 + 3 + 4 = 12
    state value = 9 - 12 = -3

    Remember that the height and width of the board may vary."""
    if breakthrough_game.isTerminal:
        return breakthrough_game.winner * 9999 
    else:
        board = breakthrough_game.board
        pos1 = 0
        neg1 = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 1:
                    pos1 += i+1
                elif board[i][j] == -1:
                    neg1 += len(board) - i
        return pos1-neg1

def breakthroughBetterEval(breakthrough_game):
    """A heuristic that generally wins agains breakthroughBasicEval.
    This must be a static evaluation function (no search allowed).

    Returns +9999 if player +1 has won.
    Returns -9999 if player -1 has won.

    Otherwise finds the square of the rank of each piece (number of rows onto the board it
    has advanced), sums these square ranks for each player, and
    returns (player +1's sum of ranks) - (player -1's sum of ranks).

    An example on a 5x3 board:
    ------------
    |  0  1  1 |  <-- player +1 has (2 piece*(square(rank1)))
    |  1 -1  1 |  <-- +1 has (2 piece * (square(rank2))); -1 has (1 piece * (square(rank 4)))
    |  0  1 -1 |  <-- +1 has (1 piece * (square(rank 3)); -1 has (1 piece *  (square(rank 3))
    | -1  0  0 |  <-- -1 has (1 piece * (square(rank 2))
    | -1 -1 -1 |  <-- -1 has (3 piece * (square(rank 1))
    ------------
    sum of +1's piece ranks = 1 + 1 + 4 + 4 + 9 = 19
    sum of -1's piece ranks = 1 + 1 + 1 + 4 + 9 + 16 = 32
    state value = 19 - 32 = -13

    Remember that the height and width of the board may vary.
    
    """
    if breakthrough_game.isTerminal:
        return breakthrough_game.winner * 9999
    else:
        board = breakthrough_game.board
        pos1 = 0
        neg1 = 0
        rows = len(board)
        cols = len(board[0])
        for i in range(rows):
            for j in range(cols):
                if board[i][j] == 1:
                    pos1 += i**2  
                elif board[i][j] == -1:
                    neg1 += ((rows - i) ** 2) 
        return pos1 - neg1


if __name__ == '__main__':
    """
    Create a game of Mancala.  Try 10 random moves and check that the
    heuristic is working properly. 
    """
    print("\nTESTING MANCALA HEURISTIC")
    print("-"*50)
    game1 = Mancala()
    print(game1)
    for i in range(10):
        move = choice(game1.availableMoves)
        print("\nmaking move", move)
        game1 = game1.makeMove(move)
        print(game1)
        score = mancalaBasicEval(game1)
        print("basicEval score", score)

    print("\nTESTING BREAKTHROUGH HEURISTIC")
    print("-"*50)
    game2 = Breakthrough()
    print(game2)
    for i in range(10):
        move = choice(game2.availableMoves)
        print("\nmaking move", move)
        game2 = game2.makeMove(move)
        print(game2)
        score = breakthroughBasicEval(game2)
        print("basicEval score", score)
        score2 = breakthroughBetterEval(game2)
        print("betterEval score", score2)
    

