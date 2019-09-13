##This class is a represtentation of a vertex for a graph.

class Vertex():
	def __init__(self, num: int, lat: float = 0.0, lon: float = 0.0):
		self._num = num
		self._edges = []
		self._lat = lat
		self._lon = lon
		

	#Getters
	def get_num(self) -> int:
		return self._num

	def get_edges(self) -> ['Edge']:
                ''' get the edges connected to this vertex '''
                return self._edges

	def get_lat(self) -> float:
		return self._lat

	def get_lon(self) -> float:
		return self._lon

	
	#Setters
	def add_edge(self, inEdge: 'Edge') -> None:
		self._edges.append(inEdge)

	def remove_edge(self, inEdge: 'Edge') -> None:
		self._edges.remove(inEdge)

	#Function for printing
	def __str__(self) -> str:
                ''' string representation of vertex, contains ID, coords, and it's edges '''
                return "Vertex({num}, ({lat}°, {lon}°), {edges})".format(
                        num = self._num,
                        lat = self._lat,
			lon = self._lon,
			edges = ["{num} -> {v}".format(num = self._num, v = x.get_vertices()[1].get_num()) for x in self._edges])

