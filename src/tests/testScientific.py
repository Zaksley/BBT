import os, sys
sys.path.append(os.path.abspath("src/"))

from random import randint
from utils.graphserializer import deserialize
from utils.algorithms import pathAStar
from time import perf_counter

#Save a graph with bbox 44.8073,-0.6280,44.8350,-0.5956 for test.pkl

print("Deserializing graph...")
graph = deserialize("./test.pkl")
print("Graph have been deserialized")

nodes = list(graph.getNodes())
size = len(nodes)

exp_count = 100

delta_time = 0
delta_distance = 0 # in %
exec_time = 0
distance = 0

n = 0
while n < exp_count:
    i = randint(0, size-1)
    j = randint(0, size-1)

    if i == j: continue

    print("Clearing graph...")
    graph.unmarkAll()
    print("Graph cleared")

    start = nodes[i]
    end = nodes[j]

    print(f"Start node index is {i}")
    print(f"End node index is {j}\n")

    ###    A*    ###
    print("Finding path with A*...")
    t1 = perf_counter()
    try:
        path = pathAStar(graph, start, end)
    except:
        print("No path, skipping...")
        continue
    t2 = perf_counter()
    a_time = t2 - t1
    a_distance = path[len(path)-1].getDistance()
    print(f"Path found in {a_time}s, its lenght is {a_distance}m\n")

    print("Clearing graph...")
    graph.unmarkAll()
    print("Graph cleared")

    ###    DIJKSTRA    ###
    print("Finding path with Dijkstra...")
    t1 = perf_counter()
    path = pathAStar(graph, start, end, 0)
    t2 = perf_counter()
    d_time = t2 - t1
    d_distance = path[len(path)-1].getDistance()
    print(f"Path found in {d_time}s, its lenght is {d_distance}m\n")

    delta_time += d_time - a_time
    delta_distance += ((a_distance - d_distance) / d_distance) * 100
    exec_time += (a_time + d_time) / 2
    distance += d_distance

    n += 1

avg_delta_time = delta_time / exp_count
avg_delta_distance = delta_distance / exp_count
avg_exec_time = exec_time / exp_count
avg_distance = distance / exp_count

print("\n----------------------------------\n")
print(f"Experience has been made {exp_count} times")
print(f"A* is {avg_delta_time}s faster on average than Dijkstra")
print(f"Average time of computation is {avg_exec_time}s")
print(f"Dijkstra is {avg_delta_distance}% shorter than A*")
print(f"Average path distance is {avg_distance}m")