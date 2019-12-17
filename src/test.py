from utils.graphes import *

n1 = Node(1, 10, 10, "Chez John")
n2 = Node(2, -10, 45, "Rond point")
n3 = Node(3, -500, 12, "Gare de Lyon")
n4 = Node(4, 80, -2, "Chez moi")

g = Graph({
    n1: [n2, n3],
    n2: [n1, n3, n4],
    n3: [n2, n4],
    n4: [n2]
}, "Test Graphe")

print(g)