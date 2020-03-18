import os, math, random, folium, webbrowser
from utils.graphserializer import deserialize
from utils.algorithms import *
from time import perf_counter

bxlat = 44.8333
bxlon = -0.5667

#Save a graph with bbox 44.7973,-0.6580,44.8450,-0.5856 fo bigger.pkl

#Save a graph with bbox 44.7973,-0.6580,44.8550,-0.5756 for almost bx
#    interesting nodes: 17333, 20228

print("Deserializing graph...")
graph = deserialize("./bx.pkl")
print("Graph have been deserialized")

nodes = list(graph.getNodes())
size = len(nodes)

i = 17333#random.randint(0, size-1)
j = 20228#random.randint(0, size-1)

start = nodes[i]
end = nodes[j]

print(f"Start is node {i}")
print(f"End is node {j}")

map = folium.Map((bxlat, bxlon), zoom_start=13)

map.add_child(folium.Marker(start.getCoordinates(), popup=str(i), tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup=str(j), tooltip='End'))

print("Finding path with A*...")
t1 = perf_counter()
path = pathAStar(graph, start, end, 1.05)
t2 = perf_counter()
distance = path[len(path)-1].getDistance()
print(f"Path found in {t2-t1}s\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    edge = graph.edgeBetween(path[i], path[i+1])

    #Safety color
    c = 'red'
    if edge.getSafety() == "safe":  c = 'green'
    elif edge.getSafety() == "normal":  c = 'blue'
    elif edge.getSafety() == "unsafe": c = 'orange'
    elif edge.getSafety() == "very_unsafe": c = 'black'

    #Comfort color
        
    map.add_child(folium.PolyLine([coord1, coord2], color=c))

print("Path have been drawn")

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('file://' + os.path.abspath('./map.html'))