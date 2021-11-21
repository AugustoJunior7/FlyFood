import random
from itertools import permutations
from sklearn.utils import shuffle
from random import randint

file = open('input', 'r')  #leitura do arquivo

nlines, ncolumns = file.readline().split()
lines = file.read().splitlines()

coordinates = {}
matrix_points = []

for i in range(int(nlines)):
    line = lines[i].split()
    for j in line:
        if j != '0':
            coordinates[j] = (i, line.index(j))
            matrix_points.append(j)
matrix_points.remove('R')


def pop_generator(delivery_points, pop_size):  #gerador da população inicial
    population = []
    permutation = shuffle(list(permutations(delivery_points)))

    for i in range(pop_size):
        population.append(list(permutation[i]))

    return population


def fitness(route):  #calculo o tamanho do caminho de uma rota
    c = 0
    route_cost = 0

    route.append('R')
    route.insert(0, 'R')

    while c < len(route)-1:
        y_cost = abs(coordinates[route[c]][0] - coordinates[route[c+1]][0])
        x_cost = abs(coordinates[route[c]][1] - coordinates[route[c+1]][1])
        route_cost += x_cost + y_cost
        c += 1

    del(route[0], route[-1])

    return route_cost


def rank(population):  #função auxiliar
    population.sort(key=lambda x: x[0])
    return population


def selection(population, m):  #seleção por torneio
    most_adaptable = []
    tournament = []

    for i in range(m):
        participants = random.sample(population, 5)
        for j in participants:
            tournament.append((fitness(j), j))
        champion = rank(tournament)[0][1]
        most_adaptable.append(champion)

    return most_adaptable


def crossover(parent1, parent2):  #cruzamento realizado por PMX
    break_point = randint(1, len(parent1)-1)
    backup = parent2[:]
    offspring = []

    for child in range(2):
        for point in range(break_point):
            if parent1[point] != parent2[point]:
                temp = parent2[point]
                parent2[point] = parent1[point]

                for change_point in range(point+1, len(parent2)):
                    if parent2[point] == parent2[change_point]:
                        parent2[change_point] = temp
                        break

        offspring.append(parent2)
        parent2 = parent1
        parent1 = backup

    return offspring


def mutation(route):  #mutação por swap com 0.05% de chance de ocorrer
    if random.random() < 0.05:
        mutation_point = randint(0, len(route)-2)
        backup = route[mutation_point]

        route[mutation_point] = route[mutation_point+1]
        route[mutation_point+1] = backup

        return route


def ag(n):
    p = pop_generator(matrix_points, 100)  #população inicial
    lower_cost = float('inf')
    gc = 0                                 #contador de gerações
    lc_list = []

    while gc < n:
        s = selection(p, 20)              #seleção dos 20 mais aptos
        p = []
        for k in range(50):
            p1 = random.choice(s)        #escolha do pai 1
            p2 = random.choice(s)        #escolha do pai 2

            f1, f2 = crossover(p1, p2)   #geração de filhos

            mutation(f1)                 #chance de mutação
            mutation(f2)                 #chance de mutação

            p.append(f1)                 #reinserção da população
            p.append(f2)                 #reinserção da população

        gc += 1

        current_solution = selection(p, 1)[0]

        if fitness(current_solution) < lower_cost:
            lower_cost = fitness(current_solution)
            lc_list.append(str(lower_cost))
            best_solution = current_solution

    return best_solution, lc_list


result = ag(100)
print(' '.join(result[0]))
print(' '.join(result[1]))
