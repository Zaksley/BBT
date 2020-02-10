from grapheExamples import graphTest

path = graphTest.pathDijkstra(graphTest.getNodeByName("O"), graphTest.getNodeByName("X"))

for node in path:
    print(node.getName())

graphTest.draw()