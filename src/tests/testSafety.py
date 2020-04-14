import overpy, folium, webbrowser, os

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
        
forbidden = ['motorway', 'motorway_link', 'trunk', 'trunk_link', 'steps']

safe = ['cycleway', 'pedestrian']
normal = ['footway', 'path', 'track', 'residential', 'unclassified', 'service', 'tertiary']
unsafe = ['secondary']
very_unsafe = ['primary']

for i in range(len(query.ways)):
    tag = query.ways[i].tags["highway"]

    if tag in forbidden:
        continue
    

    c = "red"
    #Add attribut type to edge
    if tag in safe: c = 'green'
    elif tag in normal: c = 'blue'
    elif tag in unsafe: c = 'orange'
    elif tag in very_unsafe: safety = c = 'black'

    nodes = query.ways[i].nodes
    for j in range(len(nodes)-1):   
        map.add_child(folium.PolyLine([(nodes[j].lat, nodes[j].lon), (nodes[j+1].lat, nodes[j+1].lon)], color=c))

print("Start saving map...")
map.save('./map.html')
print("Map saved")
webbrowser.open_new_tab('file://' + os.path.abspath('./map.html'))