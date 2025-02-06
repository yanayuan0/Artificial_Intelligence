

import numpy as np
from Game import Game

class Nim(Game):
    """Implements the game of Nim using the Game base-class API.
    See https://en.wikipedia.org/wiki/Nim for rules.

    Can construct a game by specifying a number of pieces, or
    by copying an existing game.
    """
    def __init__(self, numSticks=10, game=None):
        if game is None: # new game
            self.sticks = numSticks
            self.turn = 1

        else: # copy constructor
            self.sticks = game.sticks
            self.turn = game.turn

    def _print_char(self, i):
        return i

    def __repr__(self):
        """A unicode representation of the board state."""
        return "\n" + str(self.sticks) + " sticks remain; turn " + str(self.turn)


    def makeMove(self, move):
        """Returns a new game instance in which move has been played.
        move is a number of sticks to pick up, valid numbers are 1, 2, 3;
        must be less than the number of sticks in the pile
        """
        if (move == 1 or move == 2 or move == 3) and ((self.sticks - move) >= 0):
            new_game = Nim(game=self)
            new_game.sticks -= move
            new_game.turn *= -1
            return new_game
        else:
            raise ValueError("makeMove got invalid value: " + str(move))

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        """List of legal moves for the current player."""
        if self.sticks >= 3:
            return [1, 2, 3]
        elif self.sticks >= 2:
            return [1, 2]
        elif self.sticks >= 1:
            return [1]

    @property
    def isTerminal(self):
        """Boolean indicating whether the game has ended."""
        return self.sticks == 0

    @property
    def winner(self):
        """+1 if the first player (maximizer) has won. -1 if the second player
        (minimizer) has won. 0 if the game is a draw. Raises an AttributeError
        if accessed on a non-terminal state."""
        if not self.isTerminal:
            raise AttributeError("Non-terminal states have no winner.")
        # player when game becomes terminal looses
        return (self.turn * -1)
