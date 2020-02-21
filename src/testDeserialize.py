import utils.graphserializer, random, folium, webbrowser
import os
import math
from utils.graphes import Edge

bxlat = 44.8333
bxlon = -0.5667

print("Deserializing graph...")
graph = utils.graphserializer.deserialize("./graph.pkl")
print("Graph have been deserialized")

nodes = graph.getNodes()
size = len(nodes)

start = nodes[random.randint(0, size-1)]
end = nodes[random.randint(0, size-1)]

map = folium.Map((bxlat, bxlon), zoom_start=13)

map.add_child(folium.Marker(start.getCoordinates(), popup='Start', tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup='End', tooltip='End'))

print("Finding path with A*...")
path = graph.pathAStar(start, end)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    edge = Edge.between(path[i], path[i+1])

    c = 'red'
    if edge.getSafety() == "safe":  c = 'green'
    elif edge.getSafety() == "normal":  c= 'blue'
    elif edge.getSafety() == "unsafe": c='orange'
    elif edge.getSafety() == "very_unsafe": c='black'
        

    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])], color=c))


print("Reset graph")
graph.unmarkAll()
for node in nodes:
    node.setDistance(math.inf)
print("Done")

"""
print("Finding path with Dijkstra...")
path = graph.pathDijkstra(start, end)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])]))
"""

print("Paths have been drawn")


print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('file://' + os.path.abspath('./map.html'))