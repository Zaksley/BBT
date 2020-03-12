import os
import webbrowser
import subprocess
import math
from .constants import R

class Node:
    """
    Summary
    =======

    A class which represent both a node in a non-oriented graph and a node in OSM data

    Parameters
    ==========

    `id` : int
        The node's OSM ID

    `latitude` : float
        The node's latitude

    `longitude` : float
        The node's longitude

    `name` : str, optionnal
        The name of the node
    """

    def __init__(self, id, latitude=0, longitude=0, name = ""):
        self._id = id
        self._coordinates = (latitude, longitude)
        self._marked = False
        self._name = name
        self._distance = math.inf
        self._cost = math.inf
        self._color = 'black'
        self._predecesor = None
        self._edges = []
        self._neighbors = []
    
    def mark(self):
        """
        Mark the node
        """

        self._marked = True

    def unmark(self):
        """
        Unmark the node
        """

        self._marked = False

    def setDistance(self, distance):
        """
        Set the node's distance to `distance` 
        """

        self._distance = distance

    def setCoordinates(self, lat, lon):
        """
        Set node's coordinates to `(lat, lon)`
        """

        self._coordinates = (lat, lon)

    def setCost(self, cost):
        """
        Set the node's cost to `cost`
        """

        self._cost = cost

    def setColor(self, color):
        """
        Set the node's color to `color` 
        """

        self._color = color

    def setPredecessor(self, predecessor):
        """
        Set the node's predecessor to `predecessor` for Dijkstra algorithm
        """

        self._predecesor = predecessor

    def isMarked(self):
        """
        Returns `True` if the node is marked and `False` else
        """

        return self._marked

    def neighborFrom(self, edge):
        """
        Returns the `Node` linked to this node by `edge`
        """

        if edge.getFirst() == self:
            return edge.getSecond()
        else:
            return edge.getFirst()

    def distanceTo(self, node):
        """
        Returns the distance from this node to `node` compared to their coordinates
        """

        (lat1, lon1) = self._coordinates
        (lat2, lon2) = node._coordinates

        #Haversine formula
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = phi2 - phi1
        dl = math.radians(lat2 - lat1)

        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

        #Euclidian approximation
        #return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * R

    def getId(self):
        """
        Returns node's ID relative to OSM data
        """

        return self._id

    def getName(self):
        """
        Returns node's ID relative to OSM data
        """

        return self._name

    def getCoordinates(self):
        """
        Returns a `Tuple` with node's latitude and longitude coordinates
        """

        return self._coordinates

    def getNeighbors(self):
        """
        Returns the `list` of node's neighbors
        """

        return self._neighbors

    def getEdges(self):
        """
        Returns the `list` of node's egdes
        """

        return self._edges

    def getDistance(self):
        """
        Returns the node's distance
        """

        return self._distance

    def getCost(self):
        """
        Returns the node's cost
        """
        
        return self._cost

    def getColor(self):
        """
        Returns the node's color
        """

        return self._color

    def getPredecessor(self):
        """
        Returns the node's predecessor
        """

        return self._predecesor

    def _addEdge(self, e):
        """
        Add an edge to the node's list of edges
        """

        self._edges.append(e)

    def _addNeighbor(self, n):
        """
        Add a node to the node's list of neighbors
        """

        self._neighbors.append(n)

class Edge:
    """
    Summary
    =======

    A class which represent both an edge in a non-oriented graph and a road/street in OSM data

    Parameters
    ==========

    `id` : int
        The edge's OSM ID

    `first` : Node
        The node where this edge starts

    `second` : Node
        The node where this edge ends

    `name` : str, optionnal
        The name of the edge
    """

    def __init__(self, id, first, second, length = 1, name = ""):
        self._id = id
        self._first = first
        self._second = second
        self._length = length
        self._marked = False
        self._name = ""
        self._safe = ""
        self._comfort = ""

    def getId(self):
        """
        Returns node's ID relative to OSM data
        """

        return self._id

    def getFirst(self):
        """
        Returns the `Node` where this edge starts
        """

        return self._first

    def getSecond(self):
        """
        Returns the `Node` where this edge ends
        """

        return self._second

    def getLength(self):
        """
        Returns the length of the edge
        """

        return self._length

    def getSafety(self):
        """
        Returns the safety of the edge
        """

        return self._safe

    def getComfort(self):
        """
        Returns the comfort of the edge
        """

        return self._comfort

    def mark(self):
        """
        Mark this edge and its reverse
        """

        #Mark this edge
        self._marked = True

        #Mark the same edge but for the other node
        Edge.between(self._second, self._first)._marked = True

    def unmark(self):
        """
        Unmark this edge and its reverse
        """

        #Unmark this edge
        self._marked = False

        #Unmark the same edge but for the other node
        Edge.between(self._second, self._first)._marked = False

    def isMarked(self):
        """
        Returns `True` if the edge is marked and `False` else
        """

        return self._marked

    @staticmethod
    def between(first, second):
        """
        Returns the `Edge` which starts from node `first` and ends to `second`

        Returns `None` if this edge does't exist
        """

        for edge in first.getEdges():
            if first.neighborFrom(edge) == second:
                return edge

        return None

    def __eq__(self, other):
        if self._first == other._first:
            return self._second == other._second
        elif self._first == other._second:
            return self._second == other._first
        else:
            return False

class Graph:
    """
    Summary
    =======

    A class which represent a graph composed of `Node` and `Edge`

    Parameters
    ==========

    `adj` : dict of `Node`
        The list of adjacency

    `name` : str, optionnal
        The name of the graph
    """

    def __init__(self, adj = {}, name = ""):
        self._nodes = []
        self._name = name

        for node in adj.keys():
            for (neighbor, length) in adj[node]:
                node._addNeighbor(neighbor)
                node._addEdge(Edge(0, node, neighbor, length))

            self._nodes.append(node)

    def getNodes(self):
        """
        Returns the list of all nodes in this graph
        """

        return self._nodes

    def getNodeByName(self, name):
        """
        Returns the `Node` of this graph which is named `name`
        """

        for node in self._nodes:
            if node.getName() == name:
                return node
        return None

    def getNodeById(self, id):
        """
        Returns the `Node` of this graph which has for id `id`
        """

        for node in self._nodes:
            if node.getId() == id:
                return node
        return None

    def unmarkAll(self):
        """
        Unmark all the nodes of the graph
        """

        for s in self._nodes:
            for e in s.getEdges():
                e.unmark()
            s.unmark()

    def _reversePath(self, start, end):
        """
        Return the path from `start` to `end` in a colored/marked graph
        """

        path = [end]

        current = end

        while current.getDistance() > 0:
            for edge in current.getEdges():
                neighbor = current.neighborFrom(edge)
                if edge.isMarked() and neighbor.getDistance() == current.getDistance() - 1:
                    path.insert(0, neighbor)
                    current = neighbor

        return path

    def path(self, start, end):
        """
        Returns an array of `Node` which represents a path, with the minimum of nodes, from node `start` to node `end`
        """
    
        waitList = []
        start.setDistance(0)
        start.mark()
        waitList.append(start)

        while len(waitList) != 0:
            current = waitList.pop(0)

            if current == end:
                return self._reversePath(start, end)
            
            for neighbor in current.getNeighbors():
                if not neighbor.isMarked():
                    neighbor.mark()
                    Edge.between(current, neighbor).mark()
                    neighbor.setDistance(current.getDistance() + 1)
                    waitList.append(neighbor)
    
    def colorByDistance(self):
        """
        Color all the nodes beside to their distance
        """
        
        colors = {
            0: 'black', 1: 'red', 2: 'green', 3: 'blue', 4: 'yellow',
            5: 'orange', 6: 'olive', 7: 'aqua', 8: 'indigo',
            9: 'tomato'
        }

        for node in self._nodes:
            distance = node.getDistance() if 0 <= node.getDistance() <= 9 else 0 
            node.setColor(colors[distance])

    def pathDijkstra(self, start, end):
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

    def pathAStar(self, start, end, weight=1):
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

    def save(self, path):
        """
        Save the graph to dot format at `path` so it can be displayed by Graphviz
        """

        f = open(path, "w", encoding="utf8")
        lines = [
            f'graph "{self._name}"' + ' {\n',
            "rankdir=LR ratio=.5 node[shape=box style=filled]\n"]
        passed_egdes = []

        for node in self._nodes:
            for edge in node.getEdges():
                neighbor = node.neighborFrom(edge)
                if not edge in passed_egdes:
                    if edge.isMarked():
                        lines.append(f'  "{node.getName()}" -- "{neighbor.getName()}" [color = red, label = {edge.getLength()}];\n')
                    else: lines.append(f'  "{node.getName()}" -- "{neighbor.getName()}" [label = {edge.getLength()}];\n')
                    passed_egdes.append(edge)
            if node.isMarked():
                lines.append(f'  "{node.getName()}" [fillcolor = {node.getColor()}, fontcolor = white, color = white, label = "{node.getName()} ({node.getDistance()})"];\n')
            else: lines.append(f'  "{node.getName()}" [fillcolor = white, fontcolor = black, color = black, label = "{node.getName()} ({node.getDistance()})"];\n')
        
        lines.append("}")

        f.writelines(lines)

    def draw(self):
        """
        Draw the graph by creating a svg file with Graphviz and opening it in the web browser
        """

        if not os.path.exists("./tmp"):
            os.mkdir("./tmp")
        self.save("./tmp/tmp.txt")

        ret = subprocess.call(['dot', '-Tsvg', '-O', os.path.abspath('./tmp/tmp.txt')])

        if ret == 0:
            webbrowser.open_new_tab("file://" + os.path.abspath('./tmp/tmp.txt.svg'))

    def addNode(self, id, lon=0, lat=0, name=""):
        """
        Add a node to this graph with the specified `id`
        """

        node = Node(id, lon, lat, name)
        self._nodes.append(node)
         
        return node

    def addEdge(self, id, first, second, weight=1, safe = "", comfort = "",  name=""):
        """
        Add an edge between this graph's nodes `first` and `second` and definite them as neighbors
        """

        edge = Edge(id, first, second, weight, name)
        edge._safe = safe
        edge._comfort = comfort
        first._addEdge(edge)
        first._addNeighbor(second)

        edge = Edge(id, second, first, weight, name)
        edge._safe = safe
        edge._comfort = comfort
        second._addEdge(edge)
        second._addNeighbor(first)