import utils.graphes
from math import sqrt, cos, sin, radians, atan2
from utils.constants import R

class OSMParser:
    """
    Static class that contains functions to convert OSM data fetched with overpy to a `Graph`
    """
    
    """@staticmethod    
    def queryToGraph(osmquery, fmap):
        #For now we consider that the data are only roads
        nodes = osmquery.nodes
        ways = osmquery.ways

        #Create the graph
        graph = utils.graphes.Graph()

        #Count how many time a node is referenced in ways
        #To gain time at the same time save coords of each node
        nodeLinks = {}
        nodeCoords = {}

        for way in ways:
            for node in way.nodes:
                if not node.id in nodeLinks.keys():
                    nodeLinks[node.id] = 1
                    nodeCoords[node.id] = (node.lat, node.lon)
                else:
                    nodeLinks[node.id] += 1

        #We determine on which nodes we wil cut a way in some edges
        cutPoints = {} #Maybe this isn't necessary

        for way in ways:
            nodesInWay = len(way.nodes)
            cutPoints[way.id] = []
            for node in way.nodes:
                #If the node is neither the start of the way nor the end
                if node.id != way.nodes[0].id and node.id != way.nodes[nodesInWay-1].id:
                    links = nodeLinks[node.id]

                    #If it has multiple references we will cut here (i.e node is a cut point)
                    if links > 1:
                        currentCutPoints = cutPoints[way.id] #Get the list of cut points for this way
                        nbOfCutPoints = len(currentCutPoints) #Save the size of this list

                        lastCutPoint = None
                        newCutPoint = None
                        #If there is already some cut points
                        if nbOfCutPoints > 0:
                            lastCutPoint = graph.getNodeById(currentCutPoints[nbOfCutPoints-1])
                        else: #This is the first cut point
                            lastCutPoint = graph.getNodeById(way.nodes[0])
                        
                        newCutPoint = graph.getNodeById(node.id)

                        if lastCutPoint == None:
                            lastCutPoint = graph.addNode(way.nodes[0].id)
                            #We set its coords
                            (lat, lon) = nodeCoords[lastCutPoint.getId()]
                            lastCutPoint.setCoordinates(lat, lon)
                        if newCutPoint == None:
                            newCutPoint = graph.addNode(node.id)
                            #We set its coords
                            (lat, lon) = nodeCoords[newCutPoint.getId()]
                            newCutPoint.setCoordinates(lat, lon)

                        (llat, llon) = lastCutPoint.getCoordinates()
                        (nlat, nlon) = newCutPoint.getCoordinates()
                        graph.addEdge(way.id, lastCutPoint, newCutPoint)
                        fmap.add_child(folium.PolyLine([(llat, llon), (nlat, nlon)]))
                        currentCutPoints.append(node.id)

                    #if links == 1:
                        #It is only a geometry node so we could compute the lenght of the edge
                        #But for now we forget it"""

    @staticmethod
    def geoDistance(lat1, lon1, lat2, lon2):
        """
        Returns the distance between two points giving their latitude and longitude
        """

        phi1 = radians(lat1)
        phi2 = radians(lat2)
        dphi = phi2 - phi1
        dl = radians(lat2 - lat1)

        a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*sin(dl/2)**2
        c = 2*atan2(sqrt(a), sqrt(1-a))

        return R * c

    @staticmethod
    def queryToGraph(query):
        """
        Convert an Overpy query into a routable graph (beta) (not optimizd)
        """

        graph = utils.graphes.Graph()
    
        for i in range(len(query.ways)):
            nodes = query.ways[i].nodes
            for j in range(len(nodes)-1):
                node = nodes[j]
                nextNode = nodes[j+1]

                first = graph.getNodeById(node.id)
                second = graph.getNodeById(nextNode.id)

                if first == None:
                    first = graph.addNode(node.id, node.lat, node.lon, node.id)
                if second == None:
                    second = graph.addNode(nextNode.id, nextNode.lat, nextNode.lon, nextNode.id)

                distance = utils.osmparser.OSMParser.geoDistance(node.lat, node.lon, nextNode.lat, nextNode.lon)
                graph.addEdge(query.ways[i].id, first, second, distance)

        return graph