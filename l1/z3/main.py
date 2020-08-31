from time import time
from random import randrange
import numpy as np

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
        # dzieki przemek
        moves = []
        direction = ['L', 'U', 'R', 'D']
        for i in range(-3, 3):
            front = direction[i]
            side = direction[i - 1]
            while True:
                if self.check_cell(side) == EXIT:
                    moves.append(self.move(side))
                    return moves
                elif self.check_cell(front) == EMPTY:
                    moves.append(self.move(front))
                else:
                    break


def minimalize_path(path, board):
    maze = Maze(board)
    for i, step in enumerate(path, start=1):
        maze.move(step)
        if maze.check_cell('H') == EXIT:
            return path[:i]
    return None


def tabu_search(max_time, board, maze):
    naive_path = maze.generate_naive_path()
    best_path = naive_path
    tabu_list = [naive_path]
    time_start = time()
    while time() - time_start < max_time:
        if len(tabu_list) > TABU_SIZE:
            tabu_list.pop(0)
        neighbours = []

        for i in range(TABU_SIZE):
            neighbour = best_path.copy()
            for j in range(len(best_path)):
                r1 = randrange(len(best_path))
                r2 = randrange(len(best_path))
                neighbour[r1], neighbour[r2] = neighbour[r2], neighbour[r1]
            neighbours.append(neighbour)

        neighbours = [minimalize_path(i, board) for i in neighbours]
        for neighbour in neighbours:
            if neighbour not in tabu_list and neighbour is not None and len(neighbour) < len(best_path):
                best_path = neighbour
        tabu_list.append(best_path)
    return best_path


if __name__ == '__main__':
    max_time, x, y = input().split()
    b = np.array([[int(char) for char in input()] for i in range(int(x))])
    m = Maze(b)
    result = tabu_search(float(max_time), b, m)
    print(f"{len(result)}\n{''.join(result)}")
