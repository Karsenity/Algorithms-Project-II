import csv
import pandas as pd

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
    routes = pd.DataFrame(routes, columns=["Airline", "Airline_ID", "Source_Airport", "Source_Airport_ID", "Destination_Airport", "Destination_Airport_ID", "Codeshare", "Stops", "Equipment"])
    return routes


def init_planes():
    with open('Resources/planes_cap.csv', 'r',newline='') as file:
        cap=[]
        data=csv.reader(file,delimiter=',')
        for row in data:
            cap.append(row)
    cap = pd.DataFrame(cap, columns=["Index", "Name", "Code3", "Code4", "Model", "Capacity"])
    return cap

def init_plane_dat():
    with open('Resources/planes.dat.txt', 'r',newline='') as file:
        data=csv.reader(file,delimiter=',')
        cap = list(data)
    cap = pd.DataFrame(cap, columns=["Name", "Code1", "Code2", "Code3"])
    return cap


def init_airports():
    with open('Resources/airports.dat', 'r', newline='', encoding='utf-8') as file:
        airports=[]
        data=csv.reader(file,delimiter=',')
        for row in data:
            airports.append(row)
    airports = pd.DataFrame(airports, columns=["ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Database_Time", "Type", "Source"])
    return airports


def init_airlines():
    with open('Resources/airlines.dat', 'r', newline='', encoding='utf-8') as file:
        data=csv.reader(file,delimiter=',')
        airlines = list(data)
    return airlines


def init_all():
    return init_routes(), init_planes(), init_airports(), init_airlines()
