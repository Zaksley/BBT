from .graphes import *

def pathDijkstra(G, start, end):
    """
    Returns an array of `Node` which represents the shortest path from node `start` to node `end` using Dijkstra algorithm
    """

    start.setDistance(0)
    current = start

    toBeTreated = [current]

    while current != end:
        current.mark() #Le noeud a une distance definitive
        toBeTreated.remove(current) #On supprime le noeud choisit de la liste des noeuds a traiter car il a maintenant une distance definitive

        #On calcule la distance des voisins et on prend le plus proche auquel on definie sa distance comme definitive (en le marquant et le supprimant de la liste a la prochaine boucle)
        best = None
        bestDist = math.inf

        for edge in current.getEdges():
            neighbor = current.neighborFrom(edge)

            if neighbor.isMarked():
                continue

            toBeTreated.append(neighbor) #On ajoute tous les noeuds a la liste de noeuds a traiter

            distance = current.getDistance() + edge.getLength()

            if distance < neighbor.getDistance(): #Si la distance etait deja calcule et plus petite alors on la touche pas
                neighbor.setDistance(distance)
                neighbor.setPredecessor(current)
            else:
                distance = neighbor.getDistance()

            if distance < bestDist:
                best = neighbor
                bestDist = distance

        #On cherche le meilleur noeud
        for node in toBeTreated:
            if best == None:
                best = node
                continue
            if node.getDistance() < best.getDistance():
                best = node

        current = best

    #Compute final path
    path = []
    predecessor = current

    while predecessor != None:
        path.insert(0, predecessor)
        predecessor = predecessor.getPredecessor()

    return path

def pathAStar(G, start, end, weight=1):
    """
    Returns an array of `Node` which represents a good path from node `start` to node `end` using A* algorithm
    """

    def appendSorted(array, node):
        if len(array) == 0:
            array.append(node)
            return

        for i in range(len(array)):
            if node.getCost() <= array[i].getCost():
                array.insert(i, node)
                return

        array.append(node)

    start.setDistance(0)
    start.setCost(0)
    current = start

    toBeTreated = [current]

    while current != end:
        current.mark() #Le noeud a une distance definitive
        toBeTreated.remove(current) #On supprime le noeud choisit de la liste des noeuds a traiter car il a maintenant une distance definitive

        #On calcule la distance des voisins et on prend le plus proche auquel on definie sa distance comme definitive (en le marquant et le supprimant de la liste a la prochaine boucle)
        for edge in current.getEdges():
            neighbor = current.neighborFrom(edge)

            if neighbor.isMarked():
                continue

            distance = current.getDistance() + edge.getLength()
            cost = distance + weight * neighbor.distanceTo(end)

            if cost < neighbor.getCost(): #Si la distance etait deja calcule et plus petite alors on la touche pas
                neighbor.setDistance(distance)
                neighbor.setCost(cost)
                neighbor.setPredecessor(current)
            #else: Bah rien

            appendSorted(toBeTreated, neighbor) #On ajoute tous les noeuds a la liste de noeuds a traiter

        current = toBeTreated[0]

    #Compute final path
    path = []
    predecessor = current

    while predecessor != None:
        path.insert(0, predecessor)
        predecessor = predecessor.getPredecessor()

    return path