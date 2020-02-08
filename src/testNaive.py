from grapheExamples import graphTest

path = graphTest.path(graphTest.getNodeByName("Début"), graphTest.getNodeByName("Fin"))

for node in path:
    print(node.getName())

graphTest.colorByDistance()
graphTest.draw()