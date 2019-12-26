import os, webbrowser, subprocess

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

    def __init__(self, id, latitude, longitude, name = ""):
        self._id = id
        self._coordinates = (latitude, longitude)
        self._marked = False
        self._name = name
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

    def _addEgde(self, e):
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

    `first` : Node
        The node where this edge starts

    `second` : Node
        The node where this edge ends

    `name` : str, optionnal
        The name of the edge
    """

    def __init__(self, first, second, weight = 1, name = ""):
        self._first = first
        self._second = second
        self._weight = weight
        self._marked = False
        self._name = ""

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

    def __init__(self, adj, name = ""):
        self._nodes = []
        self._name = name

        for node in adj.keys():
            for neighbor in adj[node]:
                node._addNeighbor(neighbor)
                node._addEgde(Edge(node, neighbor))

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

    def unmarkAll(self):
        """
        Unmark all the nodes of the graph
        """

        for s in self._nodes:
            for e in s.getEdges():
                e.unmark()
            s.unmark()
    
    def save(self, path):
        """
        Save the graph to dot format at `path` so it can be displayed by Graphviz
        """

        f = open(path, "w")
        lines = [
            f'graph "{self._name}"' + ' {\n',
            "rankdir=LR ratio=.5 node[shape=box style=filled]\n"]
        passed_egdes = []

        for node in self._nodes:
            for edge in node.getEdges():
                neighbor = node.neighborFrom(edge)
                if not edge in passed_egdes:
                    if edge.isMarked():
                        lines.append(f'  "{node.getName()}" -- "{neighbor.getName()}" [color = red];\n')
                    else: lines.append(f'  "{node.getName()}" -- "{neighbor.getName()}";\n')
                    passed_egdes.append(edge)
            if node.isMarked():
                lines.append(f'  "{node.getName()}" [fillcolor = black, fontcolor = white, color = white];\n')
            else: lines.append(f'  "{node.getName()}" [fillcolor = white, fontcolor = black, color = black];\n')
        
        lines.append("}")

        f.writelines(lines)

    @staticmethod
    def open(path):
        """
        Returns a `Graph` opened at `path`
        """

        pass

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

    def __repr__(self):
        return self.__str__()
