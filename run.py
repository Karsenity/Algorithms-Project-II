import time

from src.GetPaths import *
import networkx as nx
import numpy as np
from pprint import pprint
import matplotlib.pyplot as plt


routes = init_routes()
airports = init_airports()
planes = init_planes()
airlines = init_airlines()

ny, sf = get_airports(airports)
good_routes = get_routes(routes, ny, sf)

matrix, sink_index = create_graph(good_routes, ny, sf, planes)

##### PROBLEM 1 ########
# print(sink_index)
#graph = nx.convert_matrix.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
#pprint(nx.maximum_flow(graph, len(matrix)-1, sink_index, capacity='weight'))
##### PROBLEM 2 ########
#carrier_routes = divide_by_carrier(good_routes)
#carrier_routes_to_network(carrier_routes)

