from time import time
from random import randrange, random
import numpy as np
import sys

TABU_SIZE = 30

EMPTY = 0
WALL = 1
AGENT = 5
EXIT = 8


class Maze:

    def __init__(self, board):
        self.board = board.copy()
        agent_position = np.where(board == AGENT)
        self.current_agent_position = [int(agent_position[0]), int(agent_position[1])]
        self.moves = {'U': [-1, 0], 'R': [0, 1], 'D': [1, 0], 'L': [0, -1], 'H': [0, 0]}

    def check_cell(self, directory):
        return int(
            self.board[self.current_agent_position[0] + self.moves[directory][0], self.current_agent_position[1] +
                       self.moves[directory][1]])

    def move(self, directory):
        direction = self.moves[directory]
        new_position = [self.current_agent_position[0] + direction[0], self.current_agent_position[1] + direction[1]]
        if self.check_cell(directory) == EMPTY:
            self.board[new_position[0], new_position[1]] = AGENT
            self.board[self.current_agent_position[0], self.current_agent_position[1]] = EMPTY
            self.current_agent_position = new_position
        elif self.check_cell(directory) == EXIT:
            self.board[self.current_agent_position[0], self.current_agent_position[1]] = EMPTY
            self.current_agent_position = new_position
        return directory

    def generate_naive_path(self):
        moves = []
        direction = ['L', 'U', 'R', 'D']
        while True:
            for i in range(4):
                side = direction[i]
                if self.check_cell(side) == EXIT:
                    moves.append(self.move(side))
                    return moves
            side = direction[randrange(4)]
            if self.check_cell(side) == EMPTY:
                moves.append(self.move(side))


def minimalize_path(path, board):
    maze = Maze(board)
    for i, step in enumerate(path, start=1):
        maze.move(step)
        if maze.check_cell('H') == EXIT:
            return path[:i]
    return None


def simulated_annealing(max_time, board, maze, temperature=5000, red_factor=0.005):
    naive_path = maze.generate_naive_path()
    best_path = naive_path
    time_start = time()
    while time() - time_start < max_time and temperature > 0:
        neighbour = generate_neighbour(board, best_path)
        if len(neighbour) < len(best_path):
            best_path = neighbour
        else:
            if random() < np.e ** -((len(neighbour) - len(best_path)) / temperature):
                best_path = neighbour
        next_temperature = temperature * (1 - red_factor)
        if next_temperature > 0:
            temperature *= (1 - red_factor)
    return best_path


def generate_neighbour(board, path):
    direction = ['L', 'U', 'R', 'D']
    m = Maze(board)
    k = randrange(len(path) - 1)
    neighbour = path[:k]
    for i in neighbour:
        m.move(i)
    while True:
        for r in range(4):
            if m.check_cell(direction[r]) == EXIT:
                neighbour.append(m.move(direction[r]))
                return neighbour
        dir = direction[randrange(4)]
        if m.check_cell(dir) == EMPTY:
            neighbour.append(m.move(dir))
    return neighbour


if __name__ == '__main__':
    max_time, x, y = input().split()
    b = np.array([[int(char) for char in input()] for i in range(int(x))])
    m = Maze(b)
    result = simulated_annealing(float(max_time), b, m)
    print(len(result))
    print(''.join(result), file=sys.stderr)
