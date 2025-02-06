#! /usr/bin/env python3
########################################
# CS63: Artificial Intelligence, Lab 2
# Spring 2024, Swarthmore College
########################################


import copy
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()
    parser.add_argument("file", help="File to read for puzzle.")
    args = parser.parse_args()
    puzzle = read_puzzle(args.file)
    playGame(puzzle)

def blockingHeuristic(state):
    """Finds the goal car in the given TrafficJam state and checks how
    many spaces above it are blocked. Estimates that the distance to
    the goal is the number of rows up to the exit plus the number of
    cars blocking the exit.
    """
    count = 0
    car = 0
    for row in state.board:
        if '0' in row:
            index = 0
            for item in row:
                if item == '0':
                    break
                if item != '0':
                    index += 1
            break
        count = count + 1
    for i in range(0, count):
        if state.board[i][index] != '-':
            car += 1
    return count+car

def betterHeuristic(state):
    """A better heuristic than the blocking heuristic.

    This heuristic should be better in that:
    - It never estimates fewer moves than blockingHeuristic.
    - It sometimes estimates more moves than blockingHeuristic.
    - It never estimates more moves than are required (it's admissible).

    Our heuristic is based on the observation that if any car ahead of the
    target car has both sides occupied by either the wall or other cars.
    In this case an additional move had to be made for the blocking car
    to move out of the way. 
    """
    count = 0
    car = 0
    neighbor = 0
    for row in state.board:
        if '0' in row:
            index = 0
            for item in row:
                if item == '0':
                    break
                if item != '0':
                    index += 1
            break
        count = count + 1
    #rows ahead of the car
    for i in range(0, count):
        currcar = state.board[i][index]
        currrow = state.board[i]
        if currcar != '-':
            car += 1
            if index == 0: #leftmost col
                curri = index
                while currrow[curri] != '-' and curri <= len(currrow) -1:
                    if currrow[curri] != currcar:
                        neighbor += 1
                        break
                    curri += 1
            elif index == len(state.board[0]) -1: #rightmost col
                curri = index
                while currrow[curri] != '-' and curri >= 0:
                    if currrow[curri] != currcar:
                        neighbor += 1
                        break
                    curri -= 1
            else:
                curri = index
                right = False
                left = False
                while currrow[curri] != '-': #and curri <= len(currrow) -1
                    if currrow[curri] != currcar:
                        right = True
                        break
                    curri += 1
                curri = index
                while currrow[curri] != '-' and curri >= 0:
                    if currrow[curri] != currcar:
                        left = True
                        break
                    curri -= 1
                if (left == True) and (right == True):
                    neighbor += 1
    return count+car+neighbor


class TrafficJam:
    """
    The board represents a group of vehicles situated on a grid.  The
    vehicles may be different lengths, but are all only one grid
    square wide. Each vehicle can move either horizontally or
    vertically.  Each vehicle is given a unique number starting at 0.
    The goal of the game is to move vehicle 0 off of the grid.  Vehicle
    0 will always be positioned such that it moves vertically, thus
    whenever vehicle 0 can reach row 0 the game has been won.
    """
    def __init__(self, board, exit_col=None):
        """
        self.board: List of lists representing the game board.
        self.rows:  Integer represents the number of rows in the board.
        self.cols:  Integer represents the number of columns in the board.
        """
        self.board = board
        if exit_col is None:
            for row in self.board:
                if '0' in row:
                    self.exit_col = row.index('0')
                    break
        else:
            self.exit_col = exit_col
        self.rows = len(board)
        self.cols = len(board[0])
        self._str = None

    def __repr__(self):
        if self._str is None:
            s = "\t"*self.exit_col + " | |\n"
            s += "\n".join("\t"+"\t".join(map(str, row)) for row in self.board)
            self._str = s.expandtabs(2)
        return self._str

    def __hash__(self):
        return hash(repr(self))

    def __eq__(self, other):
        try:
            return self.board == other.board
        except AttributeError:
            return False

    def goalReached(self):
        """Returns True iff car0 is has reached the top row."""
        return '0' in self.board[0]

    def getPossibleMoves(self):
        """Returns a list of all possible moves.  Each move is
        a tuple of the form: (car, direction, (row, col)) where the
        grid location is the tip of the car that can move."""
        moves = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == '-':
                    moves += self._checkToLeft(r, c)
                    moves += self._checkToRight(r, c)
                    moves += self._checkAbove(r, c)
                    moves += self._checkBelow(r, c)
        moves.sort() # sort moves by car
        return moves

    def nextState(self, move):
        """Create a new game with the board updated according to the move."""
        nextBoard = copy.deepcopy(self.board)
        car = move[0][-1]
        direction = move[1]
        row = move[2][0]
        col = move[2][1]
        if direction == "left":
            nextBoard[row][col-1] = car
            while col < self.cols and nextBoard[row][col] == car:
                col += 1
            nextBoard[row][col-1] = '-'
        elif direction == "right":
            nextBoard[row][col+1] = car
            while col >= 0 and nextBoard[row][col] == car:
                col -= 1
            nextBoard[row][col+1] = '-'
        elif direction == "up":
            nextBoard[row-1][col] = car
            while row < self.rows and nextBoard[row][col] == car:
                row += 1
            nextBoard[row-1][col] = '-'
        elif direction == "down":
            nextBoard[row+1][col] = car
            while row >= 0 and nextBoard[row][col] == car:
                row -= 1
            nextBoard[row+1][col] = '-'
        return TrafficJam(nextBoard, self.exit_col)

    def _checkAbove(self, r, c):
        """
        Check if there is a vertical car above that can move down
        into the empty spot at location r,c.
        """
        if r-1 < 0 or self.board[r-1][c] == '-':
            return []
        num = self.board[r-1][c]
        if r-2 < 0 or self.board[r-2][c] != num:
            return []
        return [("car"+num, "down", (r-1, c))]

    def _checkBelow(self, r, c):
        """
        Check if there is a vertical car below that can move up
        into the empty spot at location r,c.
        """
        if r+1 > self.rows-1 or self.board[r+1][c] == '-':
            return []
        num = self.board[r+1][c]
        if r+2 > self.rows-1 or self.board[r+2][c] != num:
            return []
        return [("car"+num, "up", (r+1, c))]

    def _checkToLeft(self, r, c):
        """
        Check if there is a horizontal car to the left that can move
        right into the empty spot at location r,c.
        """
        if c-1 < 0 or self.board[r][c-1] == '-':
            return []
        num = self.board[r][c-1]
        if c-2 < 0 or self.board[r][c-2] != num:
            return []
        return [("car"+num, "right", (r, c-1))]

    def _checkToRight(self, r, c):
        """
        Check if there is a horizonal car to the right that can move
        left into the empty spot at location r,c.
        """
        if c+1 > self.cols-1 or self.board[r][c+1] == '-':
            return []
        num = self.board[r][c+1]
        if c+2 > self.cols-1 or self.board[r][c+2] != num:
            return []
        return [("car"+num, "left", (r, c+1))]

def read_puzzle(filename):
    with open(filename, "r") as f:
        board = [l.strip().split() for l in f]
    return TrafficJam(board)

def playGame(puzzle):
    """Allows a human user to play a game."""
    steps = 0
    while not puzzle.goalReached():
        print(puzzle)
        moves = puzzle.getPossibleMoves()
        for i in range(len(moves)):
            car, direction, location = moves[i]
            print("%s: %s %s" % (chr(ord('a')+i), car, direction))
        choice = input("Select move (or q to quit): ")
        if choice == 'q':
            return
        index = ord(choice) - ord('a')
        puzzle = puzzle.nextState(moves[index])
        steps += 1
    print(puzzle)
    print("You solved the puzzle in %d moves" % (steps))

if __name__ == '__main__':
    main()
