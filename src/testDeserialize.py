from utils.graphserializer import *

graph = deserialize("./graph.pkl")

for node in graph.getNodes():
    print(node.getId())