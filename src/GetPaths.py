
"""
makes a list of lists where each inner list is a row of the file
"""
import csv
import math
import os
import pandas as pd
from pprint import pprint


def init_routes():
    with open('Resources/routes.dat.txt', 'r', newline='') as file:
        routes=[]
        data=csv.reader(file,delimiter=',')
        for row in data:
            route=[]
            for i in range(len(row)-1):
                route.append(row[i])
            route.append(row[len(row)-1].split())
            routes.append(route)
    return routes


def init_planes():
    with open('Resources/planes_cap.csv', 'r',newline='') as file:
        cap=[]
        data=csv.reader(file,delimiter=',')
        for row in data:
            cap.append(row)
    return cap


def init_airports():
    with open('Resources/airports.dat', 'r', newline='', encoding='utf-8') as file:
        airports=[]
        data=csv.reader(file,delimiter=',')
        for row in data:
            airports.append(row)
    return airports

"""
Get the airports corresponding to NY and San Francisco
"""
def get_airports(airports):
    ny=[]
    sf=[]
    for i in range(len(airports)):
        if airports[i][2]=='New York': #If the city served is NY
            ny.append(airports[i][0]) #Append the OpenFlights ID
        elif airports[i][2]=='San Francisco':
            sf.append(airports[i][0])
    return ny, sf


def get_routes(routes, ny, sf):
    good_routes = []

    prospective_routes = [r for r in routes if r[3] in ny]

    for i in range(len(prospective_routes)):
        if prospective_routes[i][5] in sf and int(prospective_routes[i][7])<=1:
            good_routes.append([prospective_routes[i]])
        else:
            for j in range(len(routes)):
                if routes[j][3]==prospective_routes[i][5] and routes[j][5] in sf and prospective_routes[i][7]=='0' and routes[j][7]=='0':
                    good_routes.append([routes[j]])
                    break
    return good_routes


def init_airlines():
    with open('Resources/airlines.dat', 'r', newline='', encoding='utf-8') as file:
        data=csv.reader(file,delimiter=',')
        airlines = list(data)
    return airlines


# 3 and 5 are the indexes for source and destination
"""
Takes in a list of viable routes that represent edges of the graph, as well as 2 lists "ny" and "sf" which correspond
to all the airports within those areas. plane_cap is a table corresponding to the capacity of each plane.
"""
def create_graph(good_routes, ny, sf, plane_cap):
    # Find unique vertices in the graph
    unique_airports = sorted(list(set([r[0][5] for r in good_routes] + [r[0][3] for r in good_routes] + ny)))
    unique_airports.insert(0, sf[0])
    # Create adjacency matrix
    matrix = [[0 for i in range(len(unique_airports)+1)] for i in range(len(unique_airports)+1)]

    # code 3 = index 2
    for route in good_routes:
        for r in route:
            src, dest, plane_codes = r[3], r[5], r[8]
            src_index, dest_index = unique_airports.index(src), unique_airports.index(dest)
            # get capacity of current row
            capacity = max([int(cap[5]) for cap in plane_cap if cap[2] in plane_codes] + [0])
            matrix[src_index][dest_index] += capacity

    # simplify edges
    sink_index = unique_airports.index(sf[0])
    src_index = len(matrix)-1
    for v in ny:
        v_index = unique_airports.index(v)
        edges = [(i,e) for i,e in enumerate(matrix[v_index]) if e is not 0]
        if len(edges) > 2 or matrix[v_index][sink_index] == 0:
            for edge in edges:
                if edge[0] != sink_index:
                    matrix[v_index][edge[0]] = 0
                    matrix[src_index][edge[0]] = edge[1]

    # Set super-sink edges to NY with capacity infinity
    for v in ny:
        matrix[src_index][v_index] = float('inf')
    return matrix, sink_index





