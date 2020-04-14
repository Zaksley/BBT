from . import graphes
from math import sqrt, cos, sin, radians, atan2
from .constants import R

def geoDistance(lat1, lon1, lat2, lon2):
    """
    Returns the distance between two points giving their latitude and longitude
    """

    #Haversine formula
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dl = radians(lon2 - lon1)

    a = sin((phi2 - phi1)/2)**2 + cos(phi1)*cos(phi2)*sin(dl/2)**2
    c = 2*atan2(sqrt(a), sqrt(1-a))
    
    return R * c
    
def queryToGraph(query):
    """
    Convert an Overpy query into a routable graph
    """

    #Type of road 
    forbidden = ['motorway', 'motorway_link', 'trunk', 'trunk_link', 'steps']

    #Comfort
    safe = ['cycleway', 'pedestrian', 'path', 'footway']
    normal = ['track', 'residential', 'unclassified', 'service', 'tertiary']
    unsafe = ['secondary']
    very_unsafe = ['primary']

    #Safety 
    comfortable = ['cycleway', 'tertiary', 'primary', 'residential']
    medium_comfort = ['path', 'footway' ]
    uncomfortable = ['unclassified']
    very_uncomfortable = ['track']

    graph = graphes.Graph()

    current_edge_id = 0

    for i in range(len(query.ways)):
        tag = query.ways[i].tags["highway"]
        if tag in forbidden:
            continue

        safety = ""
        comfort = ""
        #Add attribut safety to edge
        if tag in safe: safety = 'safe'
        elif tag in normal: safety = 'normal'
        elif tag in unsafe: safety = 'unsafe'
        elif tag in very_unsafe: safety = 'very_unsafe'

        #Add attribut comfort to edge
        if tag in comfortable: comfort = 'comfort'
        elif tag in medium_comfort: comfort = 'medium_comfort'
        elif tag in uncomfortable: comfort = 'uncomfortable'
        elif tag in very_uncomfortable: comfort = 'very_uncomfortable'

        nodes = query.ways[i].nodes
        for j in range(len(nodes)-1):
            node = nodes[j]
            nextNode = nodes[j+1]

            first = graph.getNode(node.id)
            second = graph.getNode(nextNode.id)

            if first == None:
                first = graph.addNode(node.id, node.lat, node.lon)
            if second == None:
                second = graph.addNode(nextNode.id, nextNode.lat, nextNode.lon)

            distance = geoDistance(node.lat, node.lon, nextNode.lat, nextNode.lon)
            #graph.addEdge(query.ways[i].id, first, second, distance, safety, comfort)
            graph.addEdge(current_edge_id, first, second, distance, safety, comfort)
            current_edge_id += 1

    return graph