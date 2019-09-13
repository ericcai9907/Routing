'''
Mapping stuff for Wing ETA/Routing Engine
'''
'''
ALSO NEED SOMETHING THAT GIVES THE NEAREST NODE TO A GIVEN LAT LONG...


'''
from updatedGraph import haversine
#import pymongo
import json
from collections import deque


def Get_Nearest_Node(lat,lon, nodes):
	
	node_list = list(nodes.items())
	nearest = node_list[0]
	min_haversine = 10000000000000000
	
	for key in nodes.keys():
	    
		node_dist = haversine(lat, lon, nodes[key]['lat'], nodes[key]['lon'])
		if node_dist < min_haversine:
			min_haversine = node_dist
			nearest = nodes[key]
	
	
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

def set_distances(vertices):
	inf = float('inf')
	distances = dict()
	for key in vertices.keys():
		
		distances[key] = inf
	return distances


def set_prev(vertices):
	prev = dict()
	for key in vertices.keys():
		
		prev[key] = None
	return prev 


'''
Then set up dijkstras/ a-star for each individual route between these points
'''

def dijkstra(vertices, edges, source, dest):
	#assert source in vertices, 'Such source node doesn\'t exist'
	
	# 1. Mark all nodes unvisited and store them.
	# 2. Set the distance to zero for our initial node 
	# and to infinity for other nodes.
	inf = float('inf')
	distances = set_distances(vertices)
	previous_vertices = set_prev(vertices)
	distances[str(source['id'])] = 0
	new_vertices = vertices.copy()
	
	
	while new_vertices:
	    # 3. Select the unvisited node with the smallest distance, 
	    # it's current node now.
	    sorted_distances = sorted(distances.items(), key = lambda x: x[1])
	    
	    current_vertex = new_vertices[str(sorted_distances[0][0])]
	    
	
	    # 6. Stop, if the smallest distance 
	    # among the unvisited nodes is infinity.
	    if distances[str(current_vertex['id'])] == inf:
	        break
	
	    # 4. Find unvisited neighbors for the current node 
	    # and calculate their distances through the current node.
	    for edge in current_vertex['edge']:
	    	if str(edge['dest']) in new_vertices.keys():
		        alternative_route = distances[str(current_vertex['id'])] + edge['weight']

		        # Compare the newly calculated distance to the assigned 
		        # and save the smaller one.
		        if alternative_route < distances[str(edge['dest'])]:
		            distances[str(edge['dest'])] = alternative_route
		            previous_vertices[str(edge['dest'])] = current_vertex
	
	    # 5. Mark the current node as visited 
	    # and remove it from the unvisited set.
	    distances.pop(str(sorted_distances[0][0]))
	    del new_vertices[str(current_vertex['id'])]

	
	
	path, current_vertex = deque(), dest
	while previous_vertices[str(current_vertex['id'])] is not None:
	    path.appendleft(current_vertex)
	    current_vertex = previous_vertices[str(current_vertex['id'])]
	if path:
	    path.appendleft(current_vertex)
	return path


def pathfinder(coords : 'list of tuples of lat/lons'): # , driving : bool):
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
	
	
	
	if driving:
	    
	    Use driving maps/graphs
	    
	
	
	
	else:
	    
	    Use the full graphs with all nodes/ footpaths etc
	'''
	
	with open('uci_graph_2.txt', 'r') as graphfile:
	    graph = json.loads(graphfile.read())
	    
	
	
	source = Get_Nearest_Node(coords[0][0], coords[0][1], graph['vertices'])
	dest = Get_Nearest_Node(coords[1][0], coords[1][1], graph['vertices'])
	
	path = dijkstra(graph['vertices'], graph['edges'], source, dest)
	
	
	json_path = dict()
	
	for i in path:
	    json_path[str(i['id'])] = i
	
	json_path = json.dumps(json_path, indent = 4)
	
	
	return json_path
	
	
'''
if __name__ == '__main__':
	path = pathfinder([(33.64321, -117.82902),(33.6485432, -117.821234)])
	
	print(path)
'''


