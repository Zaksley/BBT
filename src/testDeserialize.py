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

start = nodes[random.randint(0, size-1)]
end = nodes[random.randint(0, size-1)]

map = folium.Map((bxlat, bxlon), zoom_start=13)

map.add_child(folium.Marker(start.getCoordinates(), popup='Start', tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup='End', tooltip='End'))

print("Finding path with A*...")
path = pathAStar(graph, start, end)
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
        
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])], color=c))

print("Path have been drawn")

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('file://' + os.path.abspath('./map.html'))