import time
import numpy as np


def local_search(vector, max_time, function):
    time_start = time.time()
    x = vector
    while time.time() - time_start < max_time:
        res = function(x)
        neighbours = [[x_i + np.random.uniform(-1, 1) * abs(x_i) for x_i in x]
                      for _ in range(1000)]
        for neighbour in neighbours:
            neighbour_res = function(neighbour)
            if res > neighbour_res:
                x = neighbour
                break

        else:
            return x
    else:
        return x


def happy_cat(x):
    x_norm = np.linalg.norm(x)
    return ((x_norm - 4) ** 2) ** 0.125 + 1 / 4 * (0.5 * x_norm ** 2 + sum((i for i in x))) + 1 / 2


def griewank(x):
    return 1 + 1 / 4000 * sum((x_i ** 2 for x_i in x)) - np.product(
        [np.cos(x_i / np.sqrt(i)) for i, x_i in enumerate(x, 1)])


if __name__ == '__main__':
    my_time, mode = input().split()
    my_time = int(my_time)

    if mode == '0':
        V = list(np.random.uniform(-100, 100, 4))
        result = local_search(V, my_time, happy_cat)
        print(f'{result[0]} {result[1]} {result[2]} {result[3]} {happy_cat(result)}')
    else:
        V = list(np.random.uniform(-100, 100, 4))
        result = local_search(V, my_time, griewank)
        print(f'{result[0]} {result[1]} {result[2]} {result[3]} {griewank(result)}')
