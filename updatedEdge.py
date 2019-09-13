from updatedVertex import Vertex

## This class is a representation for an edge that connects two vertices

class Edge():
	'''This class represents an edge to be used in a graph for routing.'''
	def __init__(self, num: int, source: 'Vertex', destination: 'Vertex'):
		'''Initialize the edge.'''
		self._num = num
		self._vertices = [source, destination]
		self._name = "Unnamed Street"
		self._length = 0
		self._speed = 0
		self._inter = False

	#Getters
	def get_num(self) -> int:
		'''Get the id for the edge.'''
		return self._num

	def get_vertices(self) -> ['Vertex']:
		'''Get the connected vertices in a list [source, destination].'''
		return self._vertices

	def get_source(self) -> 'Vertex':
		return self._vertices[0]

	def get_destination(self) -> 'Vertex':
		return self._vertices[1]

	def get_name(self) -> str:
		'''Get the name of the street of the edge.'''
		return self._name

	def get_length(self) -> int:
		'''Get the length (m) of the edge.'''
		return self._length

	def get_speed(self) -> int:
		'''Get the speed (mph) of the edge.'''
		return self._speed

	def is_intersection(self) -> bool:
		return self._inter

	def get_weight(self)-> float:
		if self._length and self._speed != 0:
			return self._length/self._speed * 60
		
		else: return 100000000

	#Setters
	def set_name(self, streetName: str):
		'''Set the street name.'''
		self._name = streetName

	def set_length(self, length: float):
		'''Set length using the Haversine Function. PUT IT HERE BITCH. :)'''
		self._length = length

	def set_speed(self, speed: int):
		'''Get speed from tag or reference.'''
		self._speed = speed

	def set_intersection(self, inter: bool):
		self._inter = inter

	#Function for printing
	def __str__(self) -> str:
		return "Edge({num}, {source} -> {dest}, {streetName}, {length}m, {speed} mph)".format(
			num = self._num,
			source = self._vertices[0].get_num(),
			dest = self._vertices[1].get_num(),
			streetName = self._name,
			length = self._length,
			speed = self._speed)






