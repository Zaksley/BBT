from grapheExamples import realGraph

path = realGraph.pathAStar(realGraph.getNodeByName("Début"), realGraph.getNodeByName("Fin"))

for node in path:
    print(node.getName())

realGraph.draw()