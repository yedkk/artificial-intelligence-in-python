############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Kangdong Yuan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.


import copy
import random
import math

############################################################
# Section 1: N-Queens
############################################################

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

def num_placements_all(n):
    return nCr(n * n, n)

def num_placements_one_per_row(n):
    return n**n

def n_queens_valid(board):
    visited=[-2]
    for i in board:
        if i in visited:
            return False
        else:
            if i == (visited[-1]-1) or i == (visited[-1]+1):
                return False
            else:
                visited.append(i)
    return True

def n_queens_helper(i, n, board, c1, c2):
    if i == n:
        yield list(board)
    else:
        for j in range(i, n):
            new = board[j]
            p = i + new
            q = i - new + n - 1
            if c1[p] and c2[q]:
                c1[p] = False
                c2[q] = False
                board[i], board[j] = board[j], board[i]
                for k in n_queens_helper(i + 1, n, board, c1, c2):
                    yield k
                c1[p] = True
                c2[q] = True
                board[i], board[j] = board[j], board[i]


def n_queens_solutions(n):
    board = list(range(n))
    cond1, cond2 = [], []
    for i in range(2*n):
        cond1.append(True)
        cond2.append(True)
    for i in n_queens_helper(0,n,board,cond1,cond2):
        yield i

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows=len(self.board)
        self.cols=len(self.board[0])

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        for i in range(row-1, row+2):
            if 0 <= i < self.rows:
                self.board[i][col] = not self.board[i][col]
        for j in range(col-1, col+2):
            if 0 <= j < self.cols:
                self.board[row][j] = not self.board[row][j]


    def scramble(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random()<0.5:
                    self.perform_move(i,j)

    def is_solved(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j]:
                    return False
        return True

    def copy(self):
        new = copy.deepcopy(self)
        return new

    def successors(self):
        for i in range(self.rows):
            for j in range(self.cols):
                new = copy.deepcopy(self)
                new.perform_move(i, j)
                yield (i, j), new


    def find_solution(self):
        waiting = [([], self)]
        queued_item = []
        visited = []
        if self.is_solved():
            return None
        while waiting:
            step, board = waiting[0]
            del waiting[0]
            visited.append(board.get_board())
            for (nextstep, newboard) in board.successors():
                w=newboard.get_board()
                solution = step + [nextstep]
                if newboard.is_solved():
                    return solution
                state = (solution, newboard)
                if w not in visited and w not in queued_item:
                    waiting.append(state)
                    queued_item.append(w)
        return None


    def create_puzzle(rows, cols):
        return LightsOutPuzzle([[False for col in xrange(cols)] for row in xrange(rows)])

def create_puzzle(rows, cols):
    new = []
    for i in range(rows):
        new.append([])
        for j in range(cols):
            new[i].append(False)
    return LightsOutPuzzle(new)

############################################################
# Section 3: Linear Disk Movement
############################################################

def solve_identical_disks(length, n):
    pass

def solve_distinct_disks(length, n):
    pass





