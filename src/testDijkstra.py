from grapheExamples import graphTest

path = graphTest.pathDijkstra(graphTest.getNodeByName("Début"), graphTest.getNodeByName("Fin"))

for node in path:
    print(node.getName())

graphTest.draw()