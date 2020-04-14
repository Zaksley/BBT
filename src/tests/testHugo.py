import os, sys
sys.path.append(os.path.abspath("src/"))

import overpy, folium, webbrowser, random
import utils.osmparser
import math
import requests
import decimal


### OSM part ###
api = overpy.Overpass()

#Where we center the map

bxlat = 44.8333
bxlon = -0.5667
map = folium.Map((bxlat, bxlon), zoom_start=12)

def SelectNode(point_info) :
    """
    Convert the given adress in format for the request
    """
    entry = input("Choisir votre adresse de " + point_info +" : ")
    entry = entry.split()
    separator = '+'
    adress = separator.join(entry)
    print("Your adress : ",adress)

    """
    Searching for the adress
    """
    result = requests.get('https://nominatim.openstreetmap.org/search?q=' + adress +'&format=json&countrycodes=fr').json()

    lat = decimal.Decimal(result[0]['lat'])
    lon = decimal.Decimal(result[0]['lon'])
    #adding a marker at the start
    
    return (lat, lon)

def nearNode(graph, latitude_focus, longitude_focus) :
    norme = math.inf
    nodesList = graph.getNodes()
    nodeMin = nodesList[0]
    for n in nodesList :
        (lat, lon) = n.getCoordinates()
        if  utils.osmparser.geoDistance(lat,lon,latitude_focus, longitude_focus) < norme :
            nodeMin = n
            norme = utils.osmparser.geoDistance(lat,lon,latitude_focus, longitude_focus)

    (lat, lon) = nodeMin.getCoordinates()
    return nodeMin


coords_start = SelectNode("départ")
coords_end = SelectNode("arrivée")


#Bounding box
if coords_start[0] < coords_end[0]: 
    minlat = coords_start[0] 
    maxlat = coords_end[0]
else: 
    minlat = coords_end[0] 
    maxlat = coords_start[0]

if coords_start[1] < coords_end[1]: 
    minlon = coords_start[1] 
    maxlon = coords_end[1]
else: 
    minlon = coords_end[1] 
    maxlon = coords_start[1]


print("Start querying")
tree = api.query(f"""
    way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
    (._;>;);
    out body;
    """)
print("Query's done")

print("Nodes: %i" % len(tree.nodes))
print("Ways: %i" % len(tree.ways))

print("Map created")


#Uncomment to just draw all roads
for i in range(len(tree.ways)):
    nodes = tree.ways[i].nodes
    for j in range(len(nodes)-1):
        map.add_child(folium.PolyLine([(nodes[j].lat, nodes[j].lon), (nodes[j+1].lat, nodes[j+1].lon)]))


print("Converting to graph...")
graph = utils.osmparser.queryToGraph(tree)
print("Graph converted")

nodes = graph.getNodes()
size = len(nodes)

start = nearNode(graph, coords_start[0], coords_start[1])
end = nearNode(graph, coords_end[0], coords_end[1])

map.add_child(folium.Marker(start.getCoordinates(), popup="Start", tooltip="Start"))
map.add_child(folium.Marker(end.getCoordinates(), popup='End', tooltip='End'))


"""
print("Finding path with A*...")
path = graph.pathAStar(start, end)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])], color='red'))

#Just to see where Dijkstra fail to find a path
map.save('./map.html')
webbrowser.open_new_tab('./map.html')

print("Reset graph")
graph.unmarkAll()
for node in nodes:
    node.setDistance(math.inf)
print("Done")

print("Finding path with Dijkstra...")
path = graph.pathDijkstra(start, end)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])], color='green'))

print("Paths have been drawn")
"""

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')