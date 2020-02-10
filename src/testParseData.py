import overpy, folium, webbrowser, random
import utils.osmparser

### OSM part ###
api = overpy.Overpass()

bxlat = 44.8333
bxlon = -0.5667

minlat = 44.8073
minlon = -0.6380
maxlat = 44.8150
maxlon = -0.6256

print("Start querying")
tree = api.query(f"""
    way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
    (._;>;);
    out body;
    """)
print("Query's done")

print("Nodes: %i" % len(tree.nodes))
print("Ways: %i" % len(tree.ways))

### Map part ###
map = folium.Map((bxlat, bxlon))
print("Map created")

print("Start drawing path...")

"""for i in range(len(tree.ways)):
    nodes = tree.ways[i].nodes
    for j in range(len(nodes)-1):
        map.add_child(folium.PolyLine([(nodes[j].lat, nodes[j].lon), (nodes[j+1].lat, nodes[j+1].lon)]))"""

#graph = utils.osmparser.OSMParser.queryToGraph(tree, map)

graph = utils.graphes.Graph()

for i in range(len(tree.ways)):
    nodes = tree.ways[i].nodes
    for j in range(len(nodes)-1):
        node = nodes[j]
        nextNode = nodes[j+1]

        first = graph.getNodeById(node.id)
        second = graph.getNodeById(nextNode.id)

        if first == None:
            first = graph.addNode(node.id, node.lat, node.lon, node.id)
        if second == None:
            second = graph.addNode(nextNode.id, nextNode.lat, nextNode.lon, nextNode.id)

        graph.addEdge(tree.ways[i].id, first, second)

nodes = graph.getNodes()
size = len(nodes)
print("Finding path...")
path = graph.pathDijkstra(nodes[random.randint(0, size-1)], nodes[random.randint(0, size-1)])

print(f"Path found\nIt contains {len(path)} nodes\nDrawing path...")
for i in range(len(path)-1):
    coord1 = path[i].getCoordinates()
    coord2 = path[i+1].getCoordinates()
    map.add_child(folium.PolyLine([(coord1[0], coord1[1]), (coord2[0], coord2[1])]))

#graph.draw()

print("Path have been drawned")

"""f = open("./map.osm", "r")
nodes = api.parse_xml(f.read()).get_way(169370450).nodes
f.close()

for i in range(len(nodes) - 1):
    map.add_child(folium.PolyLine([(nodes[i].lat, nodes[i].lon), (nodes[i+1].lat, nodes[i+1].lon)]))"""

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')

"""f = open("./map.osm", "r")
tree = api.parse_xml(f.read())
f.close()"""