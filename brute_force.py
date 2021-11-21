from itertools import permutations

file = open('input', 'r')

n, m = file.readline().split()
lines = file.read().splitlines()

coordinates = {}
delivery_points = []

for i in range(int(n)):
    line = lines[i].split()
    for j in line:
        if j != '0':
            coordinates[j] = (i, line.index(j))
            delivery_points.append(j)

delivery_points.remove('R')
shortest_cost = float('inf')

for k in list(permutations(delivery_points)):
    current_cost = 0
    c = 0

    k = list(k)
    k.append('R')
    k.insert(0, 'R')

    while c < len(k)-1:
        y_cost = abs(coordinates[k[c]][0] - coordinates[k[c+1]][0])
        x_cost = abs(coordinates[k[c]][1] - coordinates[k[c+1]][1])
        current_cost += x_cost + y_cost
        c += 1

    if current_cost < shortest_cost:
        shortest_cost = current_cost
        route = k

print(' '.join(route[1:-1]))
