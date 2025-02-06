########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2024, Swarthmore College
########################################

import math

class MinMaxPlayer:
    """Gets moves by depth-limited minimax search."""
    def __init__(self, boardEval, depthBound):
        self.name = "MinMax"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root

    def getMove(self, game_state):
        """Create a recursive helper function to implement Minimax, and
        call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        self.bounded_min_max(game_state, 0)
        return self.bestMove

    def bounded_min_max(self, game_state, depth):
        if depth == self.depthBound or game_state.isTerminal:
            return self.boardEval(game_state)
        # init bestValue depending on who's turn it is
        bestValue = game_state.turn * -math.inf
        for move in game_state.availableMoves:
            next_state = game_state.makeMove(move)
            # Recursive call
            value = self.bounded_min_max(next_state, depth + 1)
            if game_state.turn == 1: #Maximizer
                if value > bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
            else: #Minimizer
                if value < bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
        return bestValue

class PruningPlayer:
    """Gets moves by depth-limited minimax search with alpha-beta pruning."""
    def __init__(self, boardEval, depthBound):
        self.name = "Pruning"
        self.boardEval = boardEval   # static evaluation function
        self.depthBound = depthBound # limit of search
        self.bestMove = None         # best move from root
        
    def getMove(self, game_state):
        """Create a recursive helper function to implement AlphaBeta pruning
        and call that helper from here. Initialize bestMove to None before
        the call to helper and then return bestMove found."""
        self.pruning_min_max(game_state, 0, -math.inf, math.inf)
        return self.bestMove
        
    def pruning_min_max(self, game_state, depth, alpha, beta):
        if depth == self.depthBound or game_state.isTerminal:
            return self.boardEval(game_state)
        # init bestValue depending on who's turn it is\
        if game_state.turn == 1: #Maximizer
            bestValue = -math.inf
            for move in game_state.availableMoves:
                next_state = game_state.makeMove(move)
                value = self.pruning_min_max(next_state, depth + 1, alpha, beta)
                if value > bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
                alpha = max(alpha, bestValue)
                if beta <= alpha:
                    break
            return bestValue
        else: #Minimizer
            bestValue = math.inf
            for move in game_state.availableMoves:
                next_state = game_state.makeMove(move)
                value = self.pruning_min_max(next_state, depth + 1, alpha, beta)
                if value < bestValue:
                    bestValue = value
                    if depth == 0:
                        self.bestMove = move
                beta = min(beta, bestValue)
                if beta <= alpha:
                    break
            return bestValue