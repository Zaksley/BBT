import overpy
import pickle
import sys
import utils.osmparser
from utils.graphes import Graph

def download_save(minlat, minlon, maxlat, maxlon, path):
    """
    Download and parse OSM data to a `Graph` and save it at `path`
    """

    api = overpy.Overpass()

    print("Start querying")
    query = api.query(f"""
        way({minlat},{minlon},{maxlat},{maxlon}) ["highway"];
        (._;>;);
        out body;
    """)
    print("Query's done")
    print(f"Received: {len(query.nodes)} nodes and {len(query.ways)} ways")

    print("Parsing graph")
    graph = utils.osmparser.OSMParser.queryToGraph(query)
    print("Graph have been parsed")

    lim = sys.getrecursionlimit()
    sys.setrecursionlimit(10000)

    try:
        f = open(path, "wb")
        print("Pickling the graph")
        pickle.dump(graph, f)
        print("Graph have been pickled")
    except Exception as err:
        print(err)

    sys.setrecursionlimit(lim)    

def deserialize(path):
    try:
        f = open(path, "rb")
        graph = pickle.load(f)
        return graph

    except Exception as err:
        print(err)
        return None