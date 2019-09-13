import json
import overpass
from updatedGraph import DirectedGraph
import pymongo


'''
Last modified by Gustavo Velazquez (gustavav@uci.edu)
Wednesday, August 22, 2018

Last modified by Eric Cai (eacai@uci.edu)
Friday, August 24, 2018

added mongo stuff
'''

## Sample Bounding Box(es)
#bbox = [33.640521551, -117.8250921325, 33.643532061, -117.8215152005]
##        -117.833469,33.639107,-117.81812,33.65034
##bbox = [33.639107,-117.833469,33.65034,-117.81812]

bbox = [33.636452,-117.837332,33.651297,-117.817765]

def bBox(lst: list) -> list:
    ''' organizes the stupid bbox coords from the website '''
    boundingbox = list()
    boundingbox.append(lst[1])
    boundingbox.append(lst[0])
    boundingbox.append(lst[3])
    boundingbox.append(lst[2])
    return boundingbox

##bbox = bBox([-117.866697,33.622923,-117.797937,33.683809])

##bbox = bBox([-117.850221,33.636932,-117.830969,33.653298])


## Generate Query
api = overpass.API(timeout = 600)
mapquery = overpass.MapQuery(bbox[0], bbox[1], bbox[2], bbox[3])

## Organize Data from JSON
jsoninfo = api.get(mapquery, responseformat = 'json')
ways = [feature for feature in jsoninfo['elements'] if feature['type'] == 'way']
nodes = [feature for feature in jsoninfo['elements'] if feature['type'] == 'node']

## Create the Graph
sampleMap = DirectedGraph(list())

## Helpers
def isOneWay(way) -> bool:
    ''' return true if way is one way, false otherwise '''
    try:
        return way['tags']['oneway'] == 'yes'
    except(KeyError):
        return False

def maxSpeed(way) -> int:
    ''' returns max speed (if available) for way from Json query '''
    try:
        speed = ''.join(x for x in way['tags']['maxspeed'] if x.isdigit())
        return int(speed)
    except(KeyError):
        try:
            return determine_speed(way['tags']['highway'])
        except(KeyError):
            return 0

def nodeInfo(nodeID: int) -> 'node':
    ''' retrieves node info, given id '''
    for node in nodes:
        if node['id'] == nodeID:
            return node

def determine_speed(roadType: str) -> int:
    ''' retrieves speed for way (if available) from Json query '''
    if roadType == 'residential':
        return 25
    elif roadType == 'primary':
        return 65
    elif roadType == 'secondary':
        return 45
    elif roadType == 'tertiary':
        return 35
    else:
        return 0

def fetch_name(way) -> str:
    ''' retrieves name of way (if available) from Json query '''
    try:
        return way['tags']['name']
    except(KeyError):
        return "No name"

## Assign all the shit to the graph

def assign_map() -> None:
    # Create/assign vertices
    for node in nodes:
        if sampleMap.vertex_exists(node['id']) == False:
            sampleMap.add_vertex(node['id'], node['lat'], node['lon'])

    # Create/assign ways
    prevNode = 0
    for way in ways:
        for node in way['nodes']:
            if prevNode == 0:
                prevNode = node
            else:
                name = fetch_name(way)
                speed = maxSpeed(way)
                sampleMap.add_edge(prevNode, node, name, speed)
                # for two way streets
                if not isOneWay(way):
                    sampleMap.add_edge(node, prevNode, name, speed)
                prevNode = node
        

if __name__ == '__main__':

    '''
    for node in nodes:
        if sampleMap.vertex_exists(node['id']) == False:
            sampleMap.add_vertex(node['id'], node['lat'], node['lon'])
    '''

    assign_map()

    print('done building graph')
    print()

    vertices = sampleMap.get_vertices()
    edges = sampleMap.get_edges()

    print(len(vertices))
    print(len(edges))
    
    stored_vertices = []
    stored_edges = []

    for vertex in vertices:
        vdata = dict()

        vdata['id'] = vertex.get_num()
        vdata['lat'] = vertex.get_lat()
        vdata['lon'] = vertex.get_lon()
        vdata['edge'] = vertex.get_edges()

        stored_vertices.append(vdata)
    print('done with vertices')
    print()

    count = 1
    for edge in edges:
        edata = dict()

        edata['id'] = count
        edata['src'] = edge.get_source().get_num()
        edata['dest'] = edge.get_destination().get_num()
        edata['name'] = edge.get_name()
        edata['weight'] = edge.get_weight()

        stored_edges.append(edata)
        count+=1

    print('done with edges')
    print()
    
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')

    print('Connected to MongoDB')
    print()

    mydb = myclient["wing_test"]

    vertexCollection = mydb['UCI_BOUNDING_vertex']
    edgeCollection = mydb['UCI_BOUNDING_edge']

    vertex_ins = vertexCollection.insert_many(stored_vertices)
    edge_ins = edgeCollection.insert_many(stored_edges)
    

    print('databases')
    print(myclient.list_database_names())
    print()

    print('collections')
    print(mydb.list_collection_names())
    print()

    print('collection1 inserted:')
    print(vertex_ins.inserted_ids)
    print()

    print('collection2 inserted:')
    print(edge_ins.inserted_ids)







            
