
import json

with open('uci_graph_2.txt','r') as graphfile:
    graph = json.loads(graphfile.read())

vertices = graph['vertices']
count = 0
for key in vertices.keys():
    if count == 10:
        break
    print(key)
    count += 1


print(vertices['3638931638'])

new_vertices = vertices.copy()

print(new_vertices['3638931638'])

distances = {'2': 3, '4': 4, '5': 5}
new_distances = distances.copy()
print(new_distances)

