import random
import sys
from copy import deepcopy
from time import time

import numpy as np

VALUES = [0, 32, 64, 128, 160, 192, 223, 255]


class Block:

    def __init__(self, start_column, start_row, width, height):
        self.start_column = start_column
        self.start_row = start_row
        self.width = width
        self.height = height
        self.value = random.choice(VALUES)
        self.column_position = width * start_column
        self.row_position = height * start_row
        self.widen = False
        self.higher = False
        self.distance = None

    def count_distance(self, matrix):
        if self.distance is not None:
            return self.distance
        self.distance = 0
        for i in range(self.row_position, self.row_position + self.height):
            for j in range(self.column_position, self.column_position + self.width):
                self.distance += (matrix[i][j] - self.value) ** 2
        return self.distance

    def set_random_value(self):
        self.value = random.choice(VALUES)
        self.distance = None


class BlockMatrix:
    data = None

    def __init__(self, k, matrix):
        self.blocks = None
        self.k = k
        self.data = matrix
        self.height = np.size(self.data, 0)
        self.width = np.size(self.data, 1)
        self.width_blocks = self.width // k
        self.height_blocks = self.height // k
        self.additional_width = self.width % k
        self.additional_height = self.height % k
        self.generate_initial_matrix()

    def count_distance(self):
        distance = 0
        for row in self.blocks:
            for block in row:
                distance += block.count_distance(self.data)
        return distance / (self.height * self.width)

    def generate_initial_matrix(self):
        self.blocks = [[Block(bw, bh, k, k)
                        for bw in range(self.width_blocks)]
                       for bh in range(self.height_blocks)]

        if self.additional_width > 0:
            for i in range(self.height_blocks):
                block = self.blocks[i][-1]
                block.width = k + self.additional_width
                block.widen = True

        if self.additional_height > 0:
            for block in self.blocks[-1]:
                block.height = k + self.additional_height
                block.higher = True

    def get_neighbours(self, block, horizontal=True, vertical=True):
        x = block.start_column
        y = block.start_row
        neighbours = []

        if 0 <= x - 1 and horizontal:
            neighbour = self.blocks[y][x - 1]
            if block.height == neighbour.height and block.row_position == neighbour.row_position:
                neighbours.append(neighbour)

        if 0 <= y - 1 and vertical:
            neighbour = self.blocks[y - 1][x]
            if block.width == neighbour.width and block.column_position == neighbour.column_position:
                neighbours.append(neighbour)

        if x + 1 < self.width_blocks and horizontal:
            neighbour = self.blocks[y][x + 1]
            if block.height == neighbour.height and block.row_position == neighbour.row_position:
                neighbours.append(neighbour)

        if y + 1 < self.height_blocks and vertical:
            neighbour = self.blocks[y + 1][x]
            if block.width == neighbour.width and block.column_position == neighbour.column_position:
                neighbours.append(neighbour)

        return neighbours

    def random_block(self):
        return random.choice(random.choice(self.blocks))

    def random_different_block(self):
        different_blocks = [x for row in self.blocks for x in row if x.widen or x.higher]
        if different_blocks:
            return random.choice(different_blocks)
        else:
            return None

    def merge_and_split(self, lesser, greater):
        if lesser.column_position == greater.column_position and lesser.width == greater.width:
            greater.height -= self.additional_height
            lesser.height += self.additional_height
            greater.higher = False
            lesser.higher = True
            if lesser.row_position > greater.row_position:
                lesser.row_position -= self.additional_height
            else:
                greater.row_position += self.additional_height

        elif lesser.row_position == greater.row_position and lesser.height == greater.height:
            greater.width -= self.additional_width
            lesser.width += self.additional_width
            lesser.widen = True
            greater.widen = False
            if lesser.column_position > greater.column_position:
                lesser.column_position -= self.additional_width
            else:
                greater.column_position += self.additional_width

        lesser.distance = None
        greater.distance = None


def generate_neighbour(matrixblock):
    neighbour1 = deepcopy(matrixblock)
    neighbour2 = deepcopy(matrixblock)
    neighbour1.random_block().set_random_value()
    block = neighbour2.random_different_block()
    if block is None:
        neighbour2 = None
    else:
        neighbours = neighbour2.get_neighbours(block, block.widen, block.higher)
        if neighbours:
            neighbour2.merge_and_split(random.choice(neighbours), block)
        else:
            neighbour2 = None
    if neighbour2 is not None and neighbour2.count_distance() < neighbour1.count_distance():
        return neighbour2
    return neighbour1


def simulated_annealing(max_time, k, matrix, temperature=50000, red_factor=0.05):
    first_result = BlockMatrix(k, matrix)
    best_result = first_result
    best_distance = best_result.count_distance()
    start_time = time()
    while time() - start_time < max_time and temperature > 0:
        new_result = generate_neighbour(best_result)
        new_distance = new_result.count_distance()
        if new_distance < best_distance:
            best_result = new_result
            best_distance = new_distance
        else:
            if random.random() < np.e ** -((new_distance - best_distance) / temperature):
                best_result = new_result
                best_distance = new_distance
        temperature *= (1 - red_factor)

    return best_result


def print_result(blockmatrix):
    array_to_print = np.empty((blockmatrix.height, blockmatrix.width), np.uint8(1))
    for row in blockmatrix.blocks:
        for block in row:
            for i in range(block.row_position, block.row_position + block.height):
                for j in range(block.column_position, block.column_position + block.width):
                    array_to_print[i][j] = block.value
    for row in array_to_print:
        str_row = [str(i) for i in row]
        print(' '.join(str_row), file=sys.stderr)


if __name__ == '__main__':
    t, n, m, k = input().split()
    t, n, m, k = float(t), int(n), int(m), int(k)
    matrix = np.array([input().split() for i in range(n)], np.uint8(1))
    result = simulated_annealing(t, k, matrix)
    print(result.count_distance())
    print_result(result)
