from utils.graphes import *

#On crée 4 sommets
n1 = Node(1, 10, 10, "Chez John")
n2 = Node(2, -10, 45, "Rond point")
n3 = Node(3, -500, 12, "Gare de Lyon")
n4 = Node(4, 80, -2, "Chez moi")

#Attention: il faut que tous les voisins de chaque sommet soit renseigné sinon ca plante le markage des arettes
#On construit un graphe avec ces sommets
g = Graph({
    n1: [(n2, 10), (n3, 4)],
    n2: [(n1, 8), (n3, 8), (n4, 2)],
    n3: [(n2, 1), (n4, 4), (n1, 20)],
    n4: [(n2, 78), (n3, 40)]
}, "Test")

#On marque toutes les arettes du premier sommet du graphe
for edge in g.getNodes()[0].getEdges():
    edge.mark()

#On marque le sommet nommé: Chez moi
g.getNodeByName("Chez moi").mark()

#On dessine le graphe
g.draw()