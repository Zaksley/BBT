class Node:
    def __init__(self, id, latitude, longitude, name = ""):
        self._id = id
        self._coordinates = (latitude, longitude)
        self._marked = False
        self._name = name
        self._edges = []
        self._neighbors = []
    
    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def isMarked(self):
        return self._marked

    def neighborFrom(self, e):
        if e.getFirst() == self:
            return e.getSecond()
        else:
            return e.getFirst()

    def getId(self):
        return self._id

    def getName(self):
        return self._name

    def getCoordinates(self):
        return self._coordinates

    def getNeighbors(self):
        return self._neighbors

    def _addEgde(self, e):
        self._edges.append(e)

    def _addNeighbor(self, n):
        self._neighbors.append(n)

class Edge:
    def __init__(self, n1, n2, weight = 1, name = ""):
        self._first = n1
        self._second = n2
        self._weight = weight
        self._marked = False
        self._name = ""

    def getFirst(self):
        return self._first

    def getSecond(self):
        return self._second

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def isMarked(self):
        return self._marked

class Graph:
    def __init__(self, adj, name = ""):
        self._nodes = []
        self._name = name

        for node in adj.keys():
            for neighbor in adj[node]:
                node._addNeighbor(neighbor)
                node._addEgde(Edge(node, neighbor))

            self._nodes.append(node)

    def getNodes(self):
        return self._nodes

    def unmarkAll(self):
        for s in self._nodes:
            for e in s.getEdges():
                e.unmark()
            s.unmark()

    def __str__(self):
        string = "Name: " + self._name + "\n"
        adj = {}

        for n in self._nodes:
            current = n.getName()
            adj[current] = []

            for v in n.getNeighbors():
                adj[current].append(v.getName())

        string += str(adj)
        return string
