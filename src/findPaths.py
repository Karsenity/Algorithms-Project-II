import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.GetPaths import create_graph

"""
Get the airports corresponding to a given city
:param: pandas dataframe
:returns list of string
"""
def get_airports(airports, city):
    return airports.loc[airports["City"]==city, "ID"].tolist()


"""
Get the valid routes between 2 given cities based on our conditions
:param: pandas dataframe, list of string, list of string
:returns pandas dataframe
"""
def get_routes_(routes, ny, sf):
    routes = routes.loc[routes["Stops"] <= '1']
    # get all routes where the source is New York and add them
    prospective_routes = routes.loc[routes["Source_Airport_ID"].isin(ny)]

    # All routes from NY to SF directly
    straight_routes = prospective_routes.loc[prospective_routes["Destination_Airport_ID"].isin(sf)]

    # get all routes to SF that are one-hop from NY
    inter_route_ids = prospective_routes.loc[~prospective_routes["Destination_Airport_ID"].isin(sf), "Destination_Airport_ID"].tolist()
    inter_routes = routes.loc[routes["Source_Airport_ID"].isin(inter_route_ids)]
    inter_routes = inter_routes.loc[inter_routes["Destination_Airport_ID"].isin(sf)]

    # All routes from NY to intermediate airports
    ny_inter = prospective_routes.loc[prospective_routes["Destination_Airport_ID"].isin(inter_routes["Source_Airport_ID"].tolist())]

    #get only routes with no stops
    good_routes = pd.concat([straight_routes, ny_inter, inter_routes])
    good_routes = good_routes.loc[good_routes["Stops"] == '0']

    return good_routes

"""
Generates an adjacency matrix using a pandas dataframe
of routes, dataframe of plane capacities, and ids for
NY and SF airports
"""
def create_adj_matrix(routes, plane_cap, ny, sf, draw=False):
    # Find unique vertices in graph
    unique_airports = list(set(routes["Source_Airport_ID"].values.tolist() + routes["Destination_Airport_ID"].values.tolist()))
    routes = assign_capacities(routes, plane_cap)

    # Initialize Matrix
    matrix = [[0 for i in range(len(unique_airports)+1)] for i in range(len(unique_airports)+1)]
    src_index = len(matrix)-1
    sink_index = unique_airports.index(sf[0])

    # Find weight of each edge by summing capacity of routes corresponding to edge
    weighted_edges = routes.groupby(["Source_Airport_ID", "Destination_Airport_ID"]).sum()
    for row in weighted_edges.itertuples():
        v1, v2 = unique_airports.index(row.Index[0]), unique_airports.index(row.Index[1])
        matrix[v1][v2] = row.Capacity

    # Remove edge from NY to internode, and add edge from super-sink to internode of same weight.
    #   Also, connected supersource to all NY nodes with capacity=Infinity
    INF = 9999999
    for id in ny:
        if id in unique_airports:
            v_index = unique_airports.index(id)
            edges = [(i,e) for i,e in enumerate(matrix[v_index]) if e is not 0]
            if len(edges) > 1 or matrix[v_index][sink_index] == 0:
                for edge in edges:
                    if edge[0] != sink_index:
                        matrix[v_index][edge[0]] = 0
                        matrix[src_index][edge[0]] += edge[1]
            matrix[src_index][v_index] = INF

    if draw==True:
        draw_matrix(matrix, ny, unique_airports, sink_index)

    return np.matrix(matrix), sink_index, unique_airports

"""
Split a dataframe of routes into a dictionary of dataframes where key is the carrier """
def divide_by_carrier(good_routes):
    airline_ids = good_routes.Airline_ID.unique()

    # Separate routes into a dictionary mapping a carrier to its routes
    carrier_routes = {id:good_routes.loc[good_routes["Airline_ID"] == id] for id in airline_ids}
    return carrier_routes

#TODO Fix the default back to 0
"""
Finds the maximum capacity of a given route
:param: pandas row"""
def find_route_capacity(route, plane_cap):
    plane_codes = route.Equipment
    capacities = plane_cap.loc[plane_cap["Code3"].isin(plane_codes), "Capacity"].tolist()
    return max([int(i) for i in capacities] + [1])


"""
Adds a column to dataframe of routes with max capacity of each row
:param: pandas dataframe x2 """
def assign_capacities(routes, plane_cap):
    routes["Capacity"] = routes.apply(lambda row: find_route_capacity(row, plane_cap), axis=1)
    return routes


"""
Uses each subset of routes per carrier to find max-flow and returns all results """
def carrier_routes_to_network(carrier_routes, ny, sf, plane_cap):
    flows = {}
    for carrier in carrier_routes.keys():
        routes = carrier_routes[carrier]
        flows[carrier] = find_max_flow(routes, ny, sf, plane_cap)
    return flows


"""
Creates a maximum flow problem from a pandas dataframe and
solves it using networkx """
def find_max_flow(good_routes, ny, sf, plane_cap, draw=False):
    matrix, sink_index, v_map = create_adj_matrix(good_routes, plane_cap, ny, sf, draw=draw)
    graph = nx.convert_matrix.from_numpy_matrix(matrix, create_using=nx.DiGraph)
    return nx.maximum_flow_value(graph, len(matrix)-1, sink_index, capacity='weight')


def draw_matrix(matrix, ny, unique_airports, sink_index):
    for id in ny:
        if id in unique_airports:
            v_index = unique_airports.index(id)
            if matrix[v_index][sink_index] == 0:
                matrix = [[matrix[r][i] for i in range(len(matrix[r])) if i!=v_index] for r in range(len(matrix)) if r!=v_index]
                unique_airports.pop(v_index)
    graph = nx.convert_matrix.from_numpy_matrix(np.matrix(matrix), create_using=nx.DiGraph)
    nx.draw_networkx(graph, with_labels=True, font_weight='bold')
    plt.show()