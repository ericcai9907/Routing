import json
import overpass
import math
from updatedGraph import DirectedGraph
from multiprocessing import Pool, Process, Value
import progressbar
import time
import os
import sys

widgets=[
    ' [', progressbar.Timer(), '] ',
    progressbar.Bar(),
    ' (', progressbar.ETA(), ') ', progressbar.Percentage(), ' ', progressbar.Counter()
]

counter = Value('i', 0)

def bBox(lst: list) -> list:
    ''' organizes the stupid bbox coords from the website '''
    boundingbox = list()
    boundingbox.append(lst[1])
    boundingbox.append(lst[0])
    boundingbox.append(lst[3])
    boundingbox.append(lst[2])
    return boundingbox

## Generate API Call
api = overpass.API(timeout = 600)

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

def assign_map(nodes, ways, sampleMap) -> None:
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

def make_edges(edges : list) :
    list_of_edges = []
    count = 1
    for edge in edges:
        edata = dict()

        edata['id'] = count
        edata['src'] = edge.get_source().get_num()
        edata['dest'] = edge.get_destination().get_num()
        edata['name'] = edge.get_name()
        edata['weight'] = edge.get_weight()

        list_of_edges.append(edata)
        count +=1
    return list_of_edges

## Generate Query

def generateQuery(bbox: list) -> None:
    ''' given coordinates for a small bounding box will create a graph and store all
        its information in a text file with its coordinates in the directory of
        this file'''
    
    mapquery = overpass.MapQuery(bbox[0], bbox[1], bbox[2], bbox[3])
    jsoninfo = api.get(mapquery, responseformat = 'json')
    ways = [feature for feature in jsoninfo['elements'] if feature['type'] == 'way']
    nodes = [feature for feature in jsoninfo['elements'] if feature['type'] == 'node']

    ## Create Graph
    currentMap = DirectedGraph(list())
    assign_map(nodes, ways, currentMap)

    ## Create Data To-Store
    vertices = currentMap.get_vertices()
    edges = currentMap.get_edges()

    stored_vertices = dict()
    stored_edges = dict()
    for vertex in vertices:
        vdata = dict()

        vdata['id'] = vertex.get_num()
        vdata['lat'] = vertex.get_lat()
        vdata['lon'] = vertex.get_lon()
        vdata['edge'] = make_edges(vertex.get_edges())
        
        stored_vertices[vertex.get_num()] = vdata
    
    stored_edges = make_edges(edges)
    graph = dict()

    graph['vertices'] = stored_vertices
    graph['edges'] = stored_edges
    counter.value += 1
    name = './MapFiles/{}_{}_{}_{}.json'.format(bbox[0], bbox[1], bbox[2], bbox[3])    
    with open(name, 'w+') as outfile:
        json.dump(graph,outfile)
    

def createBoxes(bbox: list, rows: int, columns: int) -> [[list]]:
    parentBox = bBox(bbox)
    ceiling = parentBox[2]
    wall = parentBox[1]
    childBoxes = list()
    dlat = math.fabs(parentBox[2] - parentBox[0])
    dlong = math.fabs(parentBox[1] - parentBox[3])
    for r in range(1, rows + 1):
        for c in range(1, columns +1):
            childbox = [ceiling - ((dlat/rows) * r), wall + ((dlong/columns) * (c - 1)),
                        ceiling - ((dlat/rows) * (r - 1)), wall + ((dlong/columns) * c)]
            childBoxes.append(childbox)
    return childBoxes

def fbar(len_boxes, Count):
    pbar = progressbar.ProgressBar(maxval=len_boxes, widgets=widgets)
    pbar.start()
    while(Count):
        pbar.update(value=len(os.listdir('./MapFiles')))
        sys.stdout.flush()
        time.sleep(1)
    pbar.finish()

if __name__ == '__main__':
    for f in os.listdir('./MapFiles'):
        rmf = os.path.join('./MapFiles', f)
        if(os.path.exists(rmf) and f.split('.')[1] != "keep"):
            os.remove(rmf)
    Count = True
    boxes = createBoxes([-119.3571,32.381,-115.2414,34.5178], 60, 40)
    pt = Process(target=fbar, args=(len(boxes), Count))
    pt.start()
     
    with Pool(24) as p:
        p.map(generateQuery, boxes)


    Count = False
    pt.join()
