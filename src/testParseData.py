import overpy, folium, webbrowser, random
import utils.osmparser
import math

### OSM part ###
api = overpy.Overpass()

#Where we center the map
bxlat = 44.8333
bxlon = -0.5667

#Bounding box
minlat = 44.8073
minlon = -0.6280
maxlat = 44.8250
maxlon = -0.6056

print("Start querying")
tree = api.query(f"""
    way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
    (._;>;);
    out body;
    """)
print("Query's done")

print("Nodes: %i" % len(tree.nodes))
print("Ways: %i" % len(tree.ways))

map = folium.Map((bxlat, bxlon), zoom_start=12)
print("Map created")

#Uncomment to just draw all roads
"""for i in range(len(tree.ways)):
    nodes = tree.ways[i].nodes
    for j in range(len(nodes)-1):
        map.add_child(folium.PolyLine([(nodes[j].lat, nodes[j].lon), (nodes[j+1].lat, nodes[j+1].lon)]))"""

print("Converting to graph...")
graph = utils.osmparser.OSMParser.queryToGraph(tree)
print("Graph converted")

nodes = graph.getNodes()
size = len(nodes)

start = nodes[random.randint(0, size-1)]
end = nodes[random.randint(0, size-1)]

map.add_child(folium.Marker(start.getCoordinates(), popup='Start', tooltip='Start'))
map.add_child(folium.Marker(end.getCoordinates(), popup='End', tooltip='End'))

print("Finding path with A*...")
path = graph.pathAStar(start, end)
distance = path[len(path)-1].getDistance()
print(f"Path found\nIt contains {len(path)} nodes\nIts lenght is {distance}m\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])], color='red'))

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
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])]))

print("Paths have been drawn")

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')