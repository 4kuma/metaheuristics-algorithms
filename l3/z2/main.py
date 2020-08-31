import time
import random
import math
from collections import defaultdict, Counter
import sys

N = 20
T = 8
MUTATE_POSSIBILITY = 0.33


def count_score(word):
    count_letters = Counter(word)
    for letter, value in count_letters.items():
        if value > letter_count[letter]:
            return 0
    score = sum(letter_value[char] for char in word)
    if word in dictionary:
        return score
    else:
        return 0


def mutate(word):
    letters = Counter(word)
    remaining_dict = {
        char: letter_count[char] - letters[char] for char in letter_count}
    remaining = [char for char, value in remaining_dict.items() if value > 0]
    if not remaining:
        return word

    letter_a = random.choice(remaining)
    letter_b  = random.choice(remaining)
    index = random.randint(0, len(word))

    rand = random.random()
    if rand < MUTATE_POSSIBILITY:
        word = word[:index] + letter_a + word[index:]
    elif rand< MUTATE_POSSIBILITY * 2:
        word = word[:index] + letter_a + letter_b + word[index:]
    else:
        word = word[:index] + letter_b + word[index + 1:]

    return word


def recombination(parent_a, parent_b):
    a = parent_a
    b = parent_b

    l = min(len(a), len(b))
    c = random.randrange(l)
    d = random.randrange(l)

    child = a[:c] + b[c:d] + a[d]

    return child


def tournament_selection(fitnesses):
    size = len(fitnesses)
    best = random.randrange(size)
    for i in range(1, T):
        n = random.randrange(size)
        if fitnesses[n] > fitnesses[best]:
            best = n

    return best


def genetic_algorithm(max_time, first_generation):
    start = time.time()
    population = first_generation
    best_word = None
    best_fitness = sys.maxsize

    while time.time() - start < max_time:
        fitnesses = []
        genotype_fitnesses = []

        for genotype in population:
            fitness = count_score(genotype)
            fitnesses.append(fitness)
            genotype_fitnesses.append([genotype, fitness])
            if best_word is None or fitness > best_fitness:
                best_word = genotype
                best_fitness = fitness

        for _ in range(N // 2):
            index_a = tournament_selection(fitnesses)
            index_b = tournament_selection(fitnesses)
            parent_a = population[index_a]
            parent_b = population[index_b]
            child = recombination(parent_a, parent_b)
            child= mutate(child)
            genotype_fitnesses.append([child, count_score(child)])

        genotype_fitnesses = {i[0]: i[1] for i in genotype_fitnesses}
        genotype_fitnesses = [[i, genotype_fitnesses[i]] for i in genotype_fitnesses]
        genotype_fitnesses.sort(key=lambda item: item[1], reverse=True)
        population = [i[0] for i in genotype_fitnesses]
        population = population[:N]

    return best_word, best_fitness


if __name__ == "__main__":
    with open('dict.txt') as input_file:
        dictionary = set((i for i in input_file.read().split()))
    max_time, n, s = input().split()
    max_time, n, s = int(max_time), int(n), int(s)
    letter_count = defaultdict(int)
    letter_value = {}
    for _ in range(n):
        char, cost = input().split()
        letter_value[char] = int(cost)
        letter_count[char] += 1
    input_words = []
    for _ in range(s):
        input_words.append(input().strip())
    best, score = genetic_algorithm(max_time, input_words)
    print(score)
    print(best, file=sys.stderr)
