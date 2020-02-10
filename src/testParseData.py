import overpy, folium, webbrowser
from utils.osmparser import OSMParser

### OSM part ###
api = overpy.Overpass()

bxlat = 44.8333
bxlon = -0.5667

minlat = 44.8333
minlon = -0.6380
maxlat = 44.8450
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

### Map part ###
map = folium.Map((bxlat, bxlon))
print("Map created")

print("Start drawing path...")

"""for i in range(len(tree.ways)):
    nodes = tree.ways[i].nodes
    for j in range(len(nodes) - 2):
        map.add_child(folium.PolyLine([(nodes[j].lat, nodes[j].lon), (nodes[j+1].lat, nodes[j+1].lon)]))"""

graph = OSMParser.QueryToGraph(tree, map)

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
f.close()

### Graph part ###
graph = Graph.fromQuery(tree)
start = graph.getNodeById(tree.nodes[0].id)
end = graph.getNodeById(tree.nodes[2].id)
path = graph.path(start, end)

for i in range(len(path) - 1):
    map.add_child(folium.PolyLine([(path[i].getCoordinates()[0], path[i].getCoordinates()[1]), (path[i+1].getCoordinates()[0], path[i+1].getCoordinates()[1])]))"""

