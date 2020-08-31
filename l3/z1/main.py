import numpy as np
import math
import time
import random

N = 19
BINARY_COUNT = 18


def genetic_algorithm(x, e, max_time):
    start = time.time()
    best_score = yang(x, e)
    x = [np.abs(xi) * (((2 ** BINARY_COUNT) - 1) // 5) for xi in x]
    best_solution = x
    x = [''.join("{0:018b}".format(int(xi))) for xi in x]
    x = ''.join(x)
    population = generate_population() + [x]
    while time.time() - start < max_time:
        selected_genes = make_selection(population)
        recombinated_genes = make_recombination(selected_genes)
        population = population + recombinated_genes
        modified_population = []
        for genotype in population:
            genotype = list(genotype)
            for i in range(len(genotype)):
                if random.uniform(0, 1) < 0.01:
                    if genotype[i] == '0':
                        genotype[i] = '1'
                    else:
                        genotype[i] = '0'
            modified_population.append(''.join(genotype))
        sorted_population, score, solution = sort_genotypes(modified_population, e)
        population = sorted_population[:N+1]
        if score < best_score:
            best_score = score
            best_solution = solution
    return best_score, best_solution


def generate_population():
    bin_representation = ['0', '1']
    return [''.join([random.choice(bin_representation) for _ in range(BINARY_COUNT * 5)]) for _ in range(N)]


def make_selection(genes):
    selected_genes = [gene for gene in genes if random.uniform(0, 1) < 0.25]
    if len(selected_genes) % 2 == 0:
        return selected_genes
    return selected_genes[1:]


def make_recombination(genes):
    random.shuffle(genes)
    pairs = [[genes.pop(), genes.pop()] for _ in range(len(genes) // 2)]
    recombinated_genes = []
    for pair in pairs:
        i = random.randrange(BINARY_COUNT * 5)
        new_gene = pair[0][:i] + pair[1][i:]
        recombinated_genes.append(new_gene)
    return recombinated_genes


def sort_genotypes(genotypes, e):
    all_genotypes = []
    for genotype in genotypes:
        x = [convert_number(genotype[i:i + BINARY_COUNT]) for i in range(0, len(genotype), BINARY_COUNT)]
        all_genotypes.append((genotype, yang(x, e), x))
    all_genotypes.sort(key=lambda tup: tup[1])
    return [tup[0] for tup in all_genotypes], all_genotypes[0][1], all_genotypes[0][2]


def yang(x, e):
    return sum(((e[i] * (abs(x[i])) ** (i + 1)) for i in range(5)))


def convert_number(x):
    # x = "{0:018b}".format(x)
    x = x[::-1]
    summary = sum(int(x[xi]) * (2 ** xi) for xi in range(BINARY_COUNT))
    return 10 * (summary / (2 ** 18 - 1)) - 5


if __name__ == '__main__':
    inp = [float(i) for i in input().split()]
    max_time = inp[0]
    x = inp[1:6]
    e = inp[-5:]
    print(genetic_algorithm(x, e, max_time))
