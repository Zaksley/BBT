import utils.graphes, folium

class OSMParser:
    """
    Static class that contains functions to convert OSM data fetched with overpy to a `Graph`
    """
    
    @staticmethod    
    def queryToGraph(osmquery, fmap):
        """
        Convert an Overpy query to a routable `Graph`
        """

        #For now we consider that the data are only roads
        nodes = osmquery.nodes
        ways = osmquery.ways

        #Check if we actually have some data
        if nodes == None:
            raise Exception("Empty nodes data")
        if ways == None:
            raise Exception("Empty ways data")

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
                        #But for now we forget it


        return graph