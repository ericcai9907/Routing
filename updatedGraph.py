from updatedVertex import Vertex
from updatedEdge import Edge
import math


class DirectedGraph():
    ''' a directed graph '''
    
    def __init__(self, vertex_nums:[int], edges_to_add:[(int,int)] = []):
        
        #TODO:  implement the constructor, taking a list of vertex id numbers
        #       and an optional list of edges.  An edge starts at the vertex
        #       identified by tuple[0] and ends at the vertex identified by tuple[1]
        self._vertices = []
        self._edges = []
        self._edge_counter = 0
        
        for item in vertex_nums:
            v = Vertex(item)
            self._vertices.append(v)
        
        for item in edges_to_add:
            self.add_edge(item[0], item[1])

    def get_vertices(self) -> ['Vertex']:
        ''' get the vertices in this graph '''
        return self._vertices

    def get_vertex(self, vertexID: int) -> 'Vertex':
        ''' returns the vertex object with the given ID '''
        vertex_to_return = None
        for item in self._vertices:
            if item.get_num() == vertexID:
                vertex_to_return = item

        return vertex_to_return

    def get_edges(self) -> ['Edge']:
        ''' returns the edges in *this graph '''
        return self._edges

    def get_edge_by_id(self, edgeID: int) -> 'Edge':
        ''' returns the edge object with the given ID '''
        edge_to_return = None
        for item in self._edges:
            if item.get_num() == edgeID:
                edge_to_return = item

        return edge_to_return

    def get_edge_by_vertexID(self, sourceID: int, destinationID: int) -> 'Edge':
        edge_to_return = None
        for item in self._edges:
            if(item.get_source().get_num() == sourceID):
                if(item.get_destination().get_num() == destinationID):
                    edge_to_return = item

        return edge_to_return

    def add_vertex(self, vertexID: int, lat: float = 0.0, lon: float = 0.0) -> None:
        ''' adds a vertex to a graph '''
        v = Vertex(vertexID, lat, lon)
        self._vertices.append(v)

    def remove_vertex(self, vertex: int) -> None:
        ''' remove a vertex from the graph as well as it's vertices '''
        inVertex = self.get_vertex(vertex)
        vertexToDelete = None
        for item in self._vertices:
            if item.get_num() == inVertex.get_num():
                vertexToDelete = item

        edgeList = list(vertexToDelete.get_edges())
        for item in edgeList:
            item.get_vertices()[0].remove_edge(item)
            item.get_vertices()[1].remove_edge(item)
            self._edges.remove(item)

        for item in self._vertices:
            if item.get_num() == vertexToDelete.get_num():
                self._vertices.remove(item)

    def vertex_exists(self, vertex: int) -> bool:
        ''' returns true if vertex exists '''
        for item in self._vertices:
            if item.get_num() == vertex:
                return True
        return False
            

    def add_edge(self, vertex1: int, vertex2: int, name: str = "No name",
                 speed: int = 0)->None:
        ''' 
        add an edge to the graph
        '''
        self._edge_counter += 1
        source = self.get_vertex(vertex1)
        destination = self.get_vertex(vertex2)
        length = haversine(source.get_lat(), source.get_lon(),
                                destination.get_lat(), destination.get_lon())
        
        e = Edge(self._edge_counter, source, destination)
        e.set_length(length)
        e.set_speed(speed)
        e.set_name(name)
        self._edges.append(e)
        source.add_edge(e)

    def remove_edge(self, vertex: int) -> None:
        ''' remove an edge from the graph, given id '''

        inEdge = self.get_vertex(vertex)
        edgeToDelete = None
        for item in self._edges:
            if item.get_num() == inEdge.get_num():
                edgeToDelete= item

        for item in edgeToDelete.get_vertices():
            item.remove_edge(edgeToDelete)

        for item in self._edges:
            if item.get_num() == edgeToDelete.get_num():
                self._edges.remove(item)
                
def haversine(lat1:float, lng1:float, lat2:float, lng2:float) -> float:
    """
    Returns the distance between two latitute and longitude coordinates
    :param lat1: a float that represents the latitude coordinate of one point
    :param lng1: a float that represents the longitude coordinate of one point
    :param lat2: a float that represents the latitude coordinate of another point
    :param lng2: a float that represents the longitude coordinate of another point
    :return a float representing the distance between the two points in km
    """
    r = 6371 * 10**3  #meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = r * c
    return d
'''
    def pathfinder(self, start : node, end: node):
        pass


    def __str__(self) -> str:
      pass
'''
if __name__ == '__main__':
    dg = DirectedGraph([0, 1, 2, 3, 4])
    dg.add_edge(0, 1)
    dg.add_edge(1, 2)
    dg.add_edge(1, 3)
    dg.add_edge(1, 4)
