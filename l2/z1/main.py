import numpy as np
from time import time
from math import cos, pi, sqrt
import random


def simulated_annealing(x0, t, red_factor=0.005, temperature=50000):
    x = x0
    start = time()
    xp = 0
    #tu mozna zamiast red_factor dac 0
    while temperature > red_factor and time() - start < t:
        xp = generate_xp(x)
        if np.abs(salomon_function(xp)) < np.abs(salomon_function(x)):
            x = xp
        else:
            if random.random() < np.e ** -((salomon_function(xp) - salomon_function(x)) / temperature):
                x = xp
        temperature *= (1 - red_factor)
    return x, salomon_function(x)


def salomon_function(x):
    norm = sqrt(sum(i ** 2 for i in x))
    return 1 - cos(2 * pi * norm) + 0.1 * norm


def generate_xp(x):
    return [i * random.gauss(1, 0.1) for i in x]


if __name__ == '__main__':
    t, x1, x2, x3, x4 = input().split()
    v = [float(x1), float(x2), float(x3), float(x4)]
    x, fx = simulated_annealing(v, float(t))
    print(*x, fx)
