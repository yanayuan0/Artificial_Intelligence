########################################
# CS63: Artificial Intelligence, Lab 4
# Spring 2024, Swarthmore College
########################################
# NOTE: you should not need to modify this file.
########################################


class Game:
    """Base 'game' type, intended as an informal
    interface for 2-player deterministic board games.

    This class is not intended to be instanciated!  
    (Note that Python's 'duck-typing' means you technically
    don't *need* an interface, but it's still useful for
    the programmer)
    """

    def _print_char(self, i):
        return i

    def __repr__(self):
        """A unicode representation of the board state."""
        raise NotImplementedError("Interface class, should not be instanciated")


    def makeMove(self, move):
        """Returns a new game instance in which move has been played.
        """
        raise NotImplementedError("Interface class, should not be instanciated")

#The @property decorator makes it so that you can access self.availableMoves
#as a field instead of calling self.availableMoves() as a function.
    @property
    def availableMoves(self):
        """List of legal moves for the current player."""
        raise NotImplementedError("Interface class, should not be instanciated")

    @property
    def isTerminal(self):
        """Boolean indicating whether the game has ended."""
        raise NotImplementedError("Interface class, should not be instanciated")

    @property
    def winner(self):
        """+1 if the first player (maximizer) has won. -1 if the second player
        (minimizer) has won. 0 if the game is a draw. Raises an AttributeError
        if accessed on a non-terminal state."""
        raise NotImplementedError("Interface class, should not be instanciated")
