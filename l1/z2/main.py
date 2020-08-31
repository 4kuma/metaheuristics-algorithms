import time
from random import sample

TABU_SIZE = 50


def random_solution(cities_list):
    return [0] + sample(range(1, len(cities_list)), len(cities_list) - 1) + [0]


def check_cost(way, cities_list):
    visited = way[0]
    cost = 0
    for city in way[1:]:
        cost += cities_list[visited][city]
        visited = city
    return cost


def tabu_search(max_time, cities_count, cities):
    tabu_list = []
    solution = random_solution(cities)
    best_way = solution
    tabu_list.append(solution)

    time_start = time.time()
    while time.time() - time_start < max_time:
        if len(tabu_list) > TABU_SIZE:
            tabu_list.pop(0)
        x = solution
        for i in range(1, cities_count - 1):
            for j in range(1, cities_count - 1):
                if j == i:
                    continue
                way = solution.copy()
                way[i], way[j] = way[j], way[i]
                if way not in tabu_list and (check_cost(way, cities) < check_cost(x, cities)):
                    x = way
        if x not in tabu_list:
            solution = x
            tabu_list.append(solution)
        if check_cost(solution, cities) < check_cost(best_way, cities):
            best_way = solution

    return [best_way] + [check_cost(best_way, cities)]


if __name__ == "__main__":
    parameters = input()
    my_time, cities_count = [int(num) for num in parameters.split()]
    cities = [[int(num) for num in input().split()]
              for _ in range(cities_count)]

    result = tabu_search(my_time, cities_count, cities)
    result[0] = [str(i) for i in result[0]]
    print(f'{result[1]}\n{", ".join(result[0])}')
