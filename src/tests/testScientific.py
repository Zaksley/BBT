import os, sys
sys.path.append(os.path.abspath("src/"))

import math, random, folium, webbrowser
from utils.graphserializer import deserialize
from utils.algorithms import pathAStar
from time import perf_counter

bxlat = 44.8333
bxlon = -0.5667

#Save a graph with bbox 44.8073,-0.6280,44.8350,-0.5956 for test.pkl

print("Deserializing graph...")
graph = deserialize("./test.pkl")
print("Graph have been deserialized")

nodes = list(graph.getNodes())
size = len(nodes)

i = 477#random.randint(0, size-1)
j = 6506#random.randint(0, size-1)

start = nodes[i]
end = nodes[j]

print(f"Start node index {i}")
print(f"End node index {j}")

map = folium.Map((bxlat, bxlon), zoom_start=13)

map.add_child(folium.Marker(start.getCoordinates(), popup=str(i), tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup=str(j), tooltip='End'))

###    A*    ###
print("Finding path with A*...")
t1 = perf_counter()
path = pathAStar(graph, start, end, 1)
t2 = perf_counter()
distance = path[len(path)-1].getDistance()
print(f"Path found in {t2-t1}s\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    edge = graph.edgeBetween(path[i], path[i+1])
        
    map.add_child(folium.PolyLine([coord1, coord2], color='red'))

print("Path have been drawn")

print("Clearing graph...")
graph.unmarkAll()
print("Graph cleared")

###    DIJKSTRA    ###
print("Finding path with Dijkstra...")
t1 = perf_counter()
path = pathAStar(graph, start, end, 0)
t2 = perf_counter()
distance = path[len(path)-1].getDistance()
print(f"Path found in {t2-t1}s\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    edge = graph.edgeBetween(path[i], path[i+1])
        
    map.add_child(folium.PolyLine([coord1, coord2], color='blue'))

print("Path have been drawn")

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('file://' + os.path.abspath('./map.html'))