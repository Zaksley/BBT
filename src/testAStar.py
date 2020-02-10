from grapheExamples import realGraph

path = realGraph.pathAStar(realGraph.getNodeByName("O"), realGraph.getNodeByName("X"))

for node in path:
    print(node.getName())

realGraph.draw()