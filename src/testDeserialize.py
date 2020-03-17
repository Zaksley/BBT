import os, math, random, folium, webbrowser
from utils.graphserializer import deserialize
from utils.algorithms import pathAStar

bxlat = 44.8333
bxlon = -0.5667

print("Deserializing graph...")
graph = deserialize("./bigger.pkl")
print("Graph have been deserialized")

nodes = list(graph.getNodes())
size = len(nodes)

i = random.randint(0, size-1)
j = random.randint(0, size-1)

start = nodes[i]
end = nodes[j]

map = folium.Map((bxlat, bxlon), zoom_start=13)

map.add_child(folium.Marker(start.getCoordinates(), popup=str(i), tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup=str(j), tooltip='End'))

print("Finding path with A*...")
path = pathAStar(graph, start, end, 2)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

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