import os, webbrowser, subprocess

class Node:
    def __init__(self, id, latitude, longitude, name = ""):
        self._id = id
        self._coordinates = (latitude, longitude)
        self._marked = False
        self._name = name
        self._edges = []
        self._neighbors = []
    
    def mark(self):
        self._marked = True

    def unmark(self):
        self._marked = False

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

    def getEdges(self):
        return self._edges

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

    def __eq__(self, other):
        if self.getFirst() == other.getFirst():
            return self.getSecond() == other.getSecond()
        elif self.getFirst() == other.getSecond():
            return self.getSecond() == other.getFirst()
        else:
            return False

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

    def getNodeByName(self, name):
        for node in self._nodes:
            if node.getName() == name:
                return node
        return None

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

    def save(self, path):
        f = open(path, "w")
        lines = [
            f'graph "{self._name}"' + ' {\n',
            "rankdir=LR ratio=.5 node[shape=box style=filled]\n"]
        passed_egdes = []

        for node in self._nodes:
            for edge in node.getEdges():
                neighbor = node.neighborFrom(edge)
                if not edge in passed_egdes:
                    lines.append(f'  "{node.getName()}" -- "{neighbor.getName()}";\n')
                    passed_egdes.append(edge)
            if node.isMarked():
                lines.append(f'  "{node.getName()}" [fillcolor = black, fontcolor = white, color = white];\n')
            else: lines.append(f'  "{node.getName()}" [fillcolor = white, fontcolor = black, color = black];\n')
        
        lines.append("}")

        f.writelines(lines)

    @staticmethod
    def open(path):
        pass

    def draw(self):
        if not os.path.exists("./tmp"):
            os.mkdir("./tmp")
        self.save("./tmp/tmp.txt")

        ret = subprocess.call(['dot', '-Tsvg', '-O', os.path.abspath('./tmp/tmp.txt')])

        if ret == 0:
            webbrowser.open_new_tab("file://" + os.path.abspath('./tmp/tmp.txt.svg'))