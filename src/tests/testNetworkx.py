import os, sys
sys.path.append(os.path.abspath("src/"))

import overpy, folium, webbrowser, random
import utils.osmparser
import networkx
import pickle
import math

#Bounding box
minlat = 44.7973
minlon = -0.6480
maxlat = 44.8450
maxlon = -0.5956

#Where we center the map
bxlat = 44.8333
bxlon = -0.5667

class Node:
    def __init__(self, id, lat=0, lon=0):
        self.id = id
        self.lat = lat
        self.lon = lon

def makeGraph():
    ### OSM part ###
    api = overpy.Overpass()

    print("Start querying...")
    query = api.query(f"""
        way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
        (._;>;);
        out body;
        """)
    print("Query's done")

    print("Nodes: %i" % len(query.nodes))
    print("Ways: %i" % len(query.ways))

    print("Parsing graph...")
    forbidden = ['motorway', 'motorway_link', 'trunk', 'trunk_link', 'steps']
    graph = networkx.Graph()

    for i in range(len(query.ways)):
        tag = query.ways[i].tags["highway"]

        if tag in forbidden:
            continue

        nodes = query.ways[i].nodes
        for j in range(len(nodes)-1):
            node = nodes[j]
            nextNode = nodes[j+1]

            first = None
            second = None

            res = [n for n in graph if n.id == node.id or n.id == nextNode.id]

            for n in res:
                if n.id == node.id:
                    first = n
                elif n.id == nextNode.id:
                    second = n

            if first == None:
                first = Node(node.id, node.lat, node.lon)
                graph.add_node(first)
            if second == None:
                second = Node(nextNode.id, nextNode.lat, nextNode.lon)
                graph.add_node(second)

            distance = utils.osmparser.geoDistance(first.lat, first.lon, second.lat, second.lon)
            graph.add_edge(first, second, weight=distance)

    print("Graph parsed")
    return graph

graph = None
try:
    print("Trying to load graph...")
    f = open("graph.pkl", "rb")
    graph = pickle.load(f)
    f.close()
    print("Graph loaded")
except Exception as err:
    print(err)
    print("Making new graph")
    graph = makeGraph()
    print("Trying to save graph...")
    
    try:
        f = open("graph.pkl", "wb")
        pickle.dump(graph, f)
        f.close()
    except Exception as err:
        print(err)
        quit()

    print("Graph saved")

map = folium.Map((bxlat, bxlon), zoom_start=12)
print("Map created")

nodes = list(graph.nodes)
size = len(nodes)

i = 28665#random.randint(0, size-1)
j = 522#random.randint(0, size-1)

print("start: " + str(i))
print("end: " + str(j))

start = nodes[i]
end = nodes[j]

map.add_child(folium.Marker((start.lat, start.lon), "Start", "Start"))
map.add_child(folium.Marker((end.lat, end.lon), "End", "End"))

print("Finding path...")
(length, path) = networkx.algorithms.shortest_paths.single_source_dijkstra(graph, start, end)
print("Path foud, it contains " + str(len(path)) + " nodes")
print("Its length is " + str(length) + "m")

for i in range(len(path)-2):
    map.add_child(folium.PolyLine([(path[i].lat, path[i].lon), (path[i+1].lat, path[i+1].lon)]))

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')

