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
    """

    def __init__(self, id, latitude=0, longitude=0):
        self._id = id
        self._lat = latitude
        self._lon = longitude
        self._marked = False
        self._distance = math.inf
        self._cost = math.inf
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

        self._lat = lat
        self._lon = lon

    def setCost(self, cost):
        """
        Set the node's cost to `cost`
        """

        self._cost = cost

    def setPredecessor(self, predecessor):
        """
        Set the node's predecessor to `predecessor` for A* algorithm
        """

        self._predecesor = predecessor

    def isMarked(self):
        """
        Returns `True` if the node is marked and `False` else
        """

        return self._marked

    def distanceTo(self, node):
        """
        Returns the distance from this node to `node` compared to their coordinates
        """

        lat1 = self._lat
        lat2 = node._lat

        #Haversine formula
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = phi2 - phi1
        dl = math.radians(lat2 - lat1)

        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
        c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

        return R * c

    def getId(self):
        """
        Returns node's ID relative to OSM data
        """

        return self._id

    def getCoordinates(self):
        """
        Returns a `Tuple` with node's latitude and longitude coordinates
        """

        return (self._lat, self._lon)

    def getNeighbors(self):
        """
        Returns the `list` of node's neighbors' id
        """

        return self._neighbors

    def getEdges(self):
        """
        Returns the `list` of node's egdes' id
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

    def getPredecessor(self):
        """
        Returns the node's predecessor
        """

        return self._predecesor

    def _addEdge(self, id):
        """
        Add the edge id `id` to the node's list of edges
        """

        self._edges.append(id)

    def _addNeighbor(self, id):
        """
        Add the node id `id` to the node's list of neighbors
        """

        self._neighbors.append(id)

    def __eq__(self, other):
        if other == None: return False
        else: return self._id == other._id

    def __lt__(self, other):
        return self._cost < other._cost
        
    def __le__(self, other):
        return self < other or self == other

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
    """

    def __init__(self, id, first, second, length = 1):
        self._id = id
        self._first = first
        self._second = second
        self._length = length
        self._marked = False
        self._safe = ""
        self._comfort = ""

    def getId(self):
        """
        Returns node's ID relative to OSM data
        """

        return self._id

    def getFirst(self):
        """
        Returns the id of the `Node` where this edge starts
        """

        return self._first

    def getSecond(self):
        """
        Returns the id of `Node` where this edge ends
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
        Mark this edge
        """

        self._marked = True

    def unmark(self):
        """
        Unmark this edge
        """

        self._marked = False

    def isMarked(self):
        """
        Returns `True` if the edge is marked and `False` else
        """

        return self._marked

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

    `name` : str, optionnal
        The name of the graph
    """

    def __init__(self, name=""):
        self._nodes = {}
        self._edges = {}
        self._name = name

    def getNodes(self):
        """
        Returns an iterator over the node's list of this graph
        """

        return self._nodes.values()

    def getNode(self, id):
        """
        Returns the `Node` of this graph which has for id `id`

        Returns `None` if it doesn't exist
        """
        
        try:
            return self._nodes[id]
        except:
            return None

    def getEdge(self, id):
        """
        Returns the `Edge` of this graph which has for id `id`

        Returns `None` if it doesn't exist
        """
        try:
            return self._edges[id]
        except:
            return None

    def unmarkAll(self):
        """
        Unmark all the nodes adn edges of the graph
        """

        for node in self._nodes.values():
            node.unmark()

        for edge in self._edges.values():
            edge.unmark()
            

    def addNode(self, id, lon=0, lat=0):
        """
        Add a node to this graph with the specified `id`
        """

        node = Node(id, lon, lat)
        self._nodes[id] = node
         
        return node

    def addEdge(self, id, first, second, weight=1, safe="", comfort=""):
        """
        Add an edge between this graph's nodes `first` and `second`
        """

        edge = Edge(id, first.getId(), second.getId(), weight)
        edge._safe = safe
        edge._comfort = comfort
        first._addEdge(id)
        first._addNeighbor(second.getId())
        second._addEdge(id)
        second._addNeighbor(first.getId())

        self._edges[id] = edge

    def neighborFrom(self, node, edge):
        """
        Returns the `Node` which is linked to `node` by the edge `edge`
        """

        if edge.getFirst() == node.getId():
            return self._nodes[edge.getSecond()]
        else:
            return self._nodes[edge.getFirst()]

    def edgeBetween(self, first, second):
        for first_edge_id in first.getEdges():
            for second_edge_id in second.getEdges():
                if first_edge_id == second_edge_id:
                    return self._edges[first_edge_id]

        return None