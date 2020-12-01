from src.Data_Initialization import *
from src.FindPaths import *

routes, planes, airports, airlines = init_all()
ny, sf = get_airports(airports, "New York"), get_airports(airports, "San Francisco")

#### Problem 1 #####
good_routes = get_routes_(routes, ny, sf)
print("Max flow for network is: ",find_max_flow(good_routes, ny, sf, planes, draw=False))



#### PROBLEM 2 #####
carrier_routes = divide_by_carrier(good_routes)
flows = carrier_routes_to_network(carrier_routes, ny, sf, planes)

# Get the ID of the carrier who can carry the most people
v = list(flows.values())
k = list(flows.keys())
max_ID = k[v.index(max(v))]
# Turn ID into name of the carrier
max_airline = [i[1] for i in airlines if i[0]==max_ID][0]
print("{} has the highest flow of all carriers, able to move {} people from NY to SF".format(max_airline, flows[max_ID]))


