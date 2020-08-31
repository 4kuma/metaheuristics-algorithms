from time import time
from random import randrange, random, uniform, shuffle, choice
import sys
import numpy as np

T_SIZE = 4

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


def genetic_algorithm(max_time, board, maze, paths, p):
    population = paths
    best_path = None
    best_fitness = np.inf
    time_start = time()

    while time() - time_start < max_time:
        fitnesses = []
        for path in population:
            path, fitness = check_cost(path, board)
            fitnesses.append(fitness)
            if best_path is None or fitness < best_fitness:
                best_path = path
                best_fitness = fitness

        new_population = []

        for _ in range(p // 2):
            index_a = tournament_selection(fitnesses)
            index_b = tournament_selection(fitnesses)
            parent_a = population[index_a]
            parent_b = population[index_b]
            child_a, child_b = recombination(parent_a, parent_b)
            new_population += [make_mutation(child_a), make_mutation(child_b)]

        population = new_population

    return best_path, best_fitness


def check_cost(path, board):
    m = Maze(board)
    fitness = 0
    minimalized_path = []
    for direction in path:
        if fitness > len(board) * len(board[0]):
            return path, sys.maxsize
        if m.check_cell(direction) == EXIT:
            minimalized_path.append(m.move(direction))
            fitness += 1
            return minimalized_path, fitness
        if m.check_cell(direction) != WALL:
            minimalized_path.append(m.move(direction))
            fitness += 1
    return path, sys.maxsize


def make_mutation(genotype):
    i = randrange(len(genotype))
    j = randrange(len(genotype))
    genotype[i], genotype[j] = genotype[j], genotype[i]
    return genotype


def tournament_selection(fitnesses):
    p = len(fitnesses)
    best = randrange(p)
    for i in range(1, T_SIZE):
        n = randrange(p)
        if fitnesses[n] < fitnesses[best]:
            best = n
    return best


def recombination(parent_a, parent_b):
    a = parent_a.copy()
    b = parent_b.copy()
    i = min(len(a), len(b))
    c = randrange(i)
    d = randrange(i)
    if c > d:
        c, d = d, c
    if c != d:
        for i in range(c, d):
            a[i], b[i] = a[i], b[i]
    return a, b


if __name__ == '__main__':
    max_time, x, y, s, p = input().split()
    b = np.array([[int(char) for char in input()] for i in range(int(x))])
    paths = [[char for char in input()] for _ in range(int(s))]
    m = Maze(b)
    result, best_fitness = genetic_algorithm(float(max_time), b, m, paths, int(p))
    print(best_fitness)
    print(''.join(result), file=sys.stderr)
