'''
Mapping stuff for Wing ETA/Routing Engine
'''
'''
ALSO NEED SOMETHING THAT GIVES THE NEAREST NODE TO A GIVEN LAT LONG...


'''
from updatedGraph import haversine
import pymongo



def Get_Nearest_Node(lat,lon, nodes):
	
	nearest = nodes[0]
	min_haversine = 10000000000000000

	for node in nodes:
		node_dist = haversine(lat, lon, node.lat, node.lon)
		if node_dist < min_haversine:
			nearest = node


	return nearest
	

"""
Vicinity Checker for grouping use

"""


def vicinity_checker():

	pass




'''
This is the path finding algorithm for the Routing Engine

Working on:
Determining Walking vs Driving
order grouping
how to deal with recalculations/rerouting
detours
stitching graphs
eliminating unnecessary nodes
better storage methods... 
dijkstar...
files vs db

...

NEED TAGS FOR WHETHER OR NOT THIS IS A WALKING DELIVERY VS DRIVING

LANDMARKS FOR SIGNFICANT BUILDINGS AND WHATNOT FOR SMALLER BOUDNING BOXES OR NECESSARY LOCATIONS

WALKING PATHS HAVE SPECIAL TAGS... COORDINATES, WE NEED SPEEDS FOR THESE WALKPATHS

GET BETTER AT ROUTING ON CAMPUS ROADS/PATHS BUILDINGS

How Are we getting the grouping data...

How to deal with Fulfiller accepting or denying enroute orders...

What is the best way of storing data for traversal/query?

What info do we have about buildings and whatnot in node data of uci etc.



This needs to have access to the databases or given lists of vertices and edges..
in terms of stitching, we would be able to just work with the database 

'''


myclient = pymongo.MongoClient('mongodb://localhost:27017/')

print('Connected to MongoDB')
print()

mydb = myclient["wing_test"]

vertexCollection = mydb['UCI_BOUNDING_vertex']
edgeCollection = mydb['UCI_BOUNDING_edge']





def pathfinder(coords : 'list of tuples' , driving : bool):
	'''
	This is the path finding algorithm for the routing engine 
	This function must be preceded by a connection with the Mongodb database for graph info
	@params list of coords
	@return the shortest path that exists 
	'''

	'''
	if there is more than one set of coords we need to sort them so we can get them in the most efficient order

	'''
	'''
	if (len(coords) != 1):
		srcs = []
		dests = []

	'''

	if driving:
		'''
		Use driving maps/graphs
		'''



	else:
		'''
		Use the full graphs with all nodes/ footpaths etc
		'''









    return 

    '''
    Then set up dijkstras/ a-star for each individual route between these points
    '''

def dijkstra(vertices, edges, source, dest):
    assert source in vertices, 'Such source node doesn\'t exist'

    # 1. Mark all nodes unvisited and store them.
    # 2. Set the distance to zero for our initial node 
    # and to infinity for other nodes.
    distances = {vertex: inf for vertex in vertices}
    previous_vertices = {
        vertex: None for vertex in vertices
    }
    distances[source] = 0
    vertices = vertices.copy()

    while vertices:
        # 3. Select the unvisited node with the smallest distance, 
        # it's current node now.
        current_vertex = min(
            vertices, key=lambda vertex: distances[vertex])

        # 6. Stop, if the smallest distance 
        # among the unvisited nodes is infinity.
        if distances[current_vertex] == inf:
            break

        # 4. Find unvisited neighbors for the current node 
        # and calculate their distances through the current node.
        for neighbour, cost in neighbours[current_vertex]:
            alternative_route = distances[current_vertex] + cost

            # Compare the newly calculated distance to the assigned 
            # and save the smaller one.
            if alternative_route < distances[neighbour]:
                distances[neighbour] = alternative_route
                previous_vertices[neighbour] = current_vertex

        # 5. Mark the current node as visited 
        # and remove it from the unvisited set.
        vertices.remove(current_vertex)


    path, current_vertex = deque(), dest
    while previous_vertices[current_vertex] is not None:
        path.appendleft(current_vertex)
        current_vertex = previous_vertices[current_vertex]
    if path:
        path.appendleft(current_vertex)
    return path