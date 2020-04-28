from collections import deque
from bisect import insort_left

def pathAStar(G, start, end, weight=1, safety_func=lambda edge: 1):
    """
    Returns an array of `Node` which represents a good path from node `start` to node `end` using A* algorithm
    """

    start.setDistance(0)
    start.setCost(0)
    current = start

    toBeTreated = deque([current])

    while current != end:
        #On calcule la distance des voisins et on prend le plus proche auquel on definie sa distance comme definitive (en le marquant et le supprimant de la liste a la prochaine boucle)
        for edge_id in current.getEdges():

            edge = G.getEdge(edge_id)
            neighbor = G.neighborFrom(current, edge)

            if neighbor.isMarked():
                continue

            distance = current.getDistance() + edge.getLength()
            cost = safety_func(edge) * (distance + weight * neighbor.distanceTo(end))

            if cost < neighbor.getCost(): #Si la distance etait deja calcule et plus petite alors on la touche pas
                neighbor.setDistance(distance)
                neighbor.setCost(cost)
                neighbor.setPredecessor(current)

                #On insere le noeud au bon endroit ou le reinsere
                #s'il il y était déjà
                try: toBeTreated.remove(neighbor)
                except: pass
                insort_left(toBeTreated, neighbor)

        current = toBeTreated.popleft() #On supprime le noeud choisit de la liste des noeuds a traiter car il a maintenant une distance definitive
        current.mark() #Le noeud a une distance definitive

    #Compute final path
    path = []
    predecessor = current

    while predecessor != None:
        path.append(predecessor)
        predecessor = predecessor.getPredecessor()

    path.reverse()
    return path