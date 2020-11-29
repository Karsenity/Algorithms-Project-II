from src.GetPaths import *
import networkx as nx
import numpy as np
from pprint import pprint

routes = init_routes()
print("Route Example: \n\t", routes[0])

airports = init_airports()
#print("\nAirports Example: \n\t", airports[0])

planes = init_planes()
#print("\nPlanes Example: \n\t", planes[0])

ny, sf = get_airports(airports)

good_routes = get_routes(routes,ny, sf)
matrix, sink_index = create_graph(good_routes, ny, sf, planes)

print(sink_index)
graph = nx.convert_matrix.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
pprint(nx.maximum_flow(graph, len(matrix)-1, sink_index, capacity='weight'))

