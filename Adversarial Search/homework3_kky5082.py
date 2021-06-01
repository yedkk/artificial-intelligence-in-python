############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Kangdong Yuan"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import copy
from queue import PriorityQueue
from math import inf, sqrt, pow



############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board, row = [], []
    for i in range(rows):
        for j in range(cols):
            row.append((i*rows)+j+1)
        board.append(row)
        row = []
    board[rows - 1][cols - 1] = 0
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.rows=len(self.board)
        self.cols=len(self.board[0])
        self.path=[]
        self.depth=0

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        move_direction = ['up', 'down', 'left', 'right']
        position = self.find_position()
        direction = direction.lower()
        if direction in move_direction:
            if direction == "up":
                if position[0] <= 0:
                    return False
                else:
                    self.board[position[0]][position[1]], self.board[position[0] - 1][position[1]] = \
                        self.board[position[0] - 1][position[1]], self.board[position[0]][position[1]]
                    return True
            elif direction == "down":
                if position[0] == len(self.board) - 1 or position[0] == -1:
                    return False
                else:
                    self.board[position[0]][position[1]], self.board[position[0] + 1][position[1]] = \
                        self.board[position[0] + 1][position[1]], self.board[position[0]][position[1]]
                    return True
            elif direction == "left":
                if position[1] <= 0:
                    return False
                else:
                    self.board[position[0]][position[1]], self.board[position[0]][position[1] - 1] = \
                        self.board[position[0]][position[1] - 1], self.board[position[0]][position[1]]
                    return True
            elif direction == "right":
                if position[1] == len(self.board[0]) - 1 or position[1] == -1:
                    return False
                else:
                    self.board[position[0]][position[1]], self.board[position[0]][position[1] + 1] = \
                        self.board[position[0]][position[1] + 1], self.board[position[0]][position[1]]
                    return True

    def find_position(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    return (i, j)
        return (-1, -1)

    def scramble(self, num_moves):
        pass

    def is_solved(self):
        solved_board = create_tile_puzzle(self.rows, self.cols)
        return solved_board.get_board() == self.get_board()

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        move = ["up", "down", "left", "right"]
        for i in move:
            new = self.copy()
            if new.perform_move(i):
                yield i, new

    def find_solutions_iddfs(self):
        limit = 1
        while True:
            solutions = list(self.iddfs_helper(limit, [], self))
            if len(solutions) >= 1:
                break
            limit += 1
        for i in solutions:
            yield i

    def iddfs_helper(self, limit, moves, board):
        if limit <= 0:
            if board.is_solved():
                yield moves
        else:
            for move, new_p in board.successors():
                yield from self.iddfs_helper(limit - 1, moves + [move], new_p)

    # Required
    def find_solution_a_star(self):
        f = g = 0
        visited = []
        queue = PriorityQueue()
        path = []
        future = []
        queue.put((f, g, path, self))
        while queue:
            f, g, path, current_state = queue.get()
            visited.append(current_state.board)
            if current_state.is_solved():
                return path
            for next_move, next_state in current_state.successors():
                if next_state.board in visited:
                    continue
                queue.put((next_state.dist() + g, g + 1, path + [next_move], next_state))
        return []

    def dist(self):
        output = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    output += abs(self.rows - 1 - i) + abs(self.cols - 1 - j)
                    continue
                output += abs((self.board[i][j] - 1) % self.cols - j) + abs((self.board[i][j] - 1) // self.cols - i)
        return output




############################################################
# Section 2: Grid Navigation
############################################################

def dist(start, goal):
    return sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

def successors(current, scene):
    rows, cols, x, y = len(scene), len(scene[0]), current[0], current[1]
    next_node = []
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            if i == 0 and j == 0:
                continue
            u = x + i
            v = y + j
            if 0 <= u < rows and 0 <= v < cols and not scene[u][v]:
                next_node.append((u, v))
    return next_node


def find_path(start, goal, scene):
    queue = PriorityQueue()
    visited = []
    future = []
    cost = dist(start, goal)
    queue.put((cost, start, [start], 0))
    while queue:
        f, current, path, cost = queue.get()
        if current in visited:
            continue
        visited.append(current)
        if current == goal:
            return path
        for next_move in successors(current, scene):
            if next_move in visited:
                continue
            h = dist(next_move, goal)
            dist_next = dist(current, next_move)
            queue.put((cost + dist_next + h, next_move, path + [next_move], cost + dist_next))
    return []




############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################



def next_disk(cur_state):
    length = len(cur_state)
    result = []
    for i in range(length):
        next_state = cur_state[:]
        if cur_state[i] == -1:
            continue
        if (i+1 < length) and (cur_state[i+1] == -1):
            move, next_state[i], next_state[i+1] = (i, i+1), -1, cur_state[i]
            result.append((next_state[:], move))
            next_state = cur_state[:]
        if (i-1 >= 0) and (cur_state[i-1] == -1):
            move, next_state[i], next_state[i - 1] = (i, i - 1), -1, cur_state[i]
            result.append((next_state[:], move))
            next_state = cur_state[:]
        if (i+2 < length) and (cur_state[i+1] != -1) and (cur_state[i+2] == -1):
            move, next_state[i], next_state[i + 2] = (i, i + 2), -1, cur_state[i]
            result.append((next_state[:], move))
            next_state = cur_state[:]
        if (i-2 >= 0) and (cur_state[i-1] != -1) and (cur_state[i-2] == -1):
            move, next_state[i], next_state[i - 2] = (i, i - 2), -1, cur_state[i]
            result.append((next_state[:], move))
            next_state = cur_state[:]
    return result


def dist_disk(state, dist):
    for i in range(len(state)):
        if state[i] != -1:
            dist += abs(i - (len(state) - 1 - state[i]))
    return dist


def solve_distinct_disks(length, n):
    start = create_disk(length, n)
    goal = create_goal_disk(length, n)
    visited = []
    future = []
    visited.append(start)
    queue = PriorityQueue()
    g = dist = 0
    queue.put((dist_disk(start, dist), start, []))
    while queue:
        dist, board, path = queue.get()
        if board == goal:
            return path
        for next_move, next_state in next_disk(board):
            if next_move not in visited:
                queue.put((dist_disk(next_move, 0)+len(path)+1, next_move, path + [next_state]))
                visited.append(next_move)


def create_disk(length, n):
    l = [i for i in range(n)]
    h = [-1 for i in range(length-n)]
    return l+h


def create_goal_disk(length, n):
    l = [-1 for i in range(length-n)]
    h = [i for i in range(n-1,-1,-1)]
    return l+h

############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    return DominoesGame([[False] * cols for j in range(rows)])

class DominoesGame(object):
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(self.board)
        self.cols = len(self.board)

    def get_board(self):
        return list(self.board)

    def reset(self):
        self.board = create_dominoes_game(self.rows, self.cols).get_board()

    def is_legal_move(self, row, col, vertical):
        if vertical:
            if row + 1 < len(self.board):
                return not (self.board[row][col] or self.board[row + 1][col])
            else:
                return False
        else:
            if col + 1 < len(self.board[0]):
                return not (self.board[row][col] or self.board[row][col + 1])
            else:
                return False

    def legal_moves(self, vertical):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.is_legal_move(i, j, vertical):
                    yield (i, j)

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row + 1][col] = True
        else:
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical))
        return len(moves) == 0

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        moves = list(self.legal_moves(vertical))
        for step in moves:
            new = self.copy()
            new.perform_move(step[0], step[1], vertical)
            yield step, new

    def get_random_move(self, vertical):
        pass


    def get_best_move(self, vertical, limit):
        return self.max_value(-inf, inf, None, vertical, limit)

    def max_value(self, alpha, beta, theta, vertical, limit):
        ver = list(self.successors(vertical))
        hor = list(self.successors(not vertical))
        if limit == 0 or self.game_over(vertical):
            return theta, len(ver) - len(hor), 1
        high, low, curr_move = -inf, 0, theta
        for node, next_node in ver:
            move, h_bound, l_bound = next_node.min_value(alpha, beta, node, not vertical, limit - 1)
            low += l_bound
            if h_bound > high:
                high = h_bound
                curr_move = node
            if high >= beta:
                return curr_move, high, low
            alpha = max(alpha, high)
        return curr_move, high, low

    def min_value(self, alpha, beta, theta, vertical, limit):
        vertical_child = list(self.successors(vertical))
        hor_child = list(self.successors(not vertical))
        if limit == 0 or self.game_over(vertical):
            return theta, len(hor_child) - len(vertical_child), 1
        high, low, step = inf, 0, theta
        for move, next_node in vertical_child:
            move, h_bound, l_bound = next_node.max_value(alpha, beta, move, not vertical, limit - 1)
            low += l_bound
            if h_bound < high:
                high = h_bound
                step = move
            if high <= alpha:
                return step, high, low
            beta = min(beta, high)
        return step, high, low


    # #Required
    # def get_best_move(self, vertical, limit):
    #     max_difference_in_move = -999999999
    #     successor = list(self.successors(vertical))
    #     for m, new_g in successor:
    #         self_moves = len(list(new_g.legal_moves(vertical)))
    #         opp_moves = len(list(new_g.legal_moves(not vertical)))
    #         difference_in_move = self_moves - opp_moves
    #         if difference_in_move > max_difference_in_move:
    #             max_difference_in_move = difference_in_move
    #             move = m
    #     return (move, max_difference_in_move, len(successor))



# b = [[False] * 3 for i in range(3)]
# g = DominoesGame(b)
# print(g.get_best_move(True, 1))
# print(g.get_best_move(True, 2))

# b = [[1,2,3], [4,0,5], [6,7,8]]
# # # b = [[4,1,2], [0,5,3], [7,8,6]]
# p = TilePuzzle(b)
# print(p.find_solution_a_star())

# scene = [[False,False,False], [False,False,False], [False,False,False]]
# print(find_path((0, 0), (2, 1), scene))
# print(find_path((0, 0), (0, 2), scene))

# print(solve_distinct_disks(4,2))