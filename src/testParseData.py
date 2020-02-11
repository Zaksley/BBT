import overpy, folium, webbrowser, random
import utils.osmparser

### OSM part ###
api = overpy.Overpass()

#Where we center the map
bxlat = 44.8333
bxlon = -0.5667

#Bounding box
minlat = 44.7973
minlon = -0.6480
maxlat = 44.8250
maxlon = -0.6156

print("Start querying")
tree = api.query(f"""
    way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
    (._;>;);
    out body;
    """)
print("Query's done")

print("Nodes: %i" % len(tree.nodes))
print("Ways: %i" % len(tree.ways))

map = folium.Map((bxlat, bxlon))
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

print("Finding path...")
path = graph.pathDijkstra(nodes[random.randint(0, size-1)], nodes[random.randint(0, size-1)])
print(f"Path found\nIt contains {len(path)} nodes\nDrawing path...")

for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])]))

print("Path have been drawned")

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')