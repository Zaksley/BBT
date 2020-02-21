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
query = api.query(f"""
    way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
    (._;>;);
    out body;
    """)
print("Query's done")

print("Nodes: %i" % len(query.nodes))
print("Ways: %i" % len(query.ways))

map = folium.Map((bxlat, bxlon), zoom_start=12)
print("Map created")

ways = query.ways
for i in range(len(ways)):
    nodes = ways[i].nodes

    startNode = nodes[0]
    nextNode = None
    for j in range(len(nodes)-1):
        nextNode = nodes[j+1]

        tag = ""
        try:
            tag = nextNode.tags["highway"]
        except:
            pass

        if tag == "crossing":
            map.add_child(folium.PolyLine([(startNode.lat, startNode.lon), (nextNode.lat, nextNode.lon)]))
            start = nextNode

    nextNode = nodes[len(nodes)-1]  
    map.add_child(folium.PolyLine([(startNode.lat, startNode.lon), (nextNode.lat, nextNode.lon)]))

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('./map.html')

