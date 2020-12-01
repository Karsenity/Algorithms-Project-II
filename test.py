import time

from src.GetPaths import *
import networkx as nx
import numpy as np
from pprint import pprint
from src.findPaths import *
import matplotlib.pyplot as plt

routes = init_routes()
airports = init_airports()
planes = init_planes()
airlines = init_airlines()
airports = pd.DataFrame(airports, columns=["ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Database_Time", "Type", "Source"])

ny, sf = get_airports(airports, "New York"), get_airports(airports, "San Francisco")

routes = pd.DataFrame(routes, columns=["Airline", "Airline_ID", "Source_Airport", "Source_Airport_ID", "Destination_Airport", "Destination_Airport_ID", "Codeshare", "Stops", "Equipment"])
planes = pd.DataFrame(planes, columns=["Index", "Name", "Code3", "Code4", "Model", "Capacity"])

good_routes = get_routes_(routes, ny, sf)

print(find_max_flow(good_routes, ny, sf, planes, draw=False))


#### PROBLEM 2 #####
#carrier_routes = divide_by_carrier(good_routes)
#flows = carrier_routes_to_network(carrier_routes, ny, sf, planes)

