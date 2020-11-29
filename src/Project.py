#Adam Gill
#Group Project 2
#11/21/2020

#Import the data as two lists: routes and planes

import csv
with open('../Resources/routes.dat.txt', 'r', newline='') as file:
    routes=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        route=[]
        for i in range(len(row)-1):
            route.append(row[i])
        route.append(row[len(row)-1].split())
        routes.append(route)



with open('../Resources/planes.dat.txt', 'r', newline='') as file:
    planes=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        planes.append(row)

'''        
with open('PlaneShit2.csv', 'r',newline='') as file:
    capacities=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        capacities.append(row)

with open('L_AIRCRAFT_TYPE.csv.csv', 'r',newline='') as file:
    names=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        names.append(row)
'''

with open('../Resources/airports.dat', 'r', newline='') as file:
    airports=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        airports.append(row)

'''
nodups=[]
for i in range(len(capacities)):
    if capacities[i] not in nodups:
        nodups.append(capacities[i])
'''

#Courtesy of Ben et al.
with open('plane_cap.csv', 'r',newline='') as file:
    cap=[]
    data=csv.reader(file,delimiter=',')
    for row in data:
        cap.append(row)


#Find all airports corresponding to NY and SF
ny=[]
sf=[]
for i in range(len(airports)):
    if airports[i][2]=='New York': #If the city served is NY
        ny.append(airports[i][0]) #Append the OpenFlights ID
    elif airports[i][2]=='San Francisco':
        sf.append(airports[i][0])

#Find all routes of length 2 or less from New York to San Francisco
"""prospectiveroutes=[]
goodroutes=[]
for i in range(len(ny)):
    for j in range(len(routes)):
        if routes[j][3]==ny[i]:
            prospectiveroutes.append(routes[j])
for i in range(len(prospectiveroutes)):
    if prospectiveroutes[i][5] in sf:
        goodroutes.append([routes[i]])
    else:
        for j in range(len(routes)):
            if routes[j][3]==prospectiveroutes[i][5] and routes[j][5] in sf:
                goodroutes.append([prospectiveroutes[i], routes[j])

#goodroutes is a list of all the routes that go from NY to SF in 1 layover or less
#Each element of goodroutes is a list of for [flight] or [flight1, flight2], where the flights are formatted as in routes.dat

#Now, figure out how many people each route can take
#routes.dat -> planes.dat -> L_AIRFRAFT_TYPE -> PlaneShit2.csv
#goodroutes -> planes -> names -> capacities
#For each route in goodroutes, the number of people carried will be the minimum of the two flights

for i in range(len(goodroutes)):
    names=[] #The names of the planes used for the two flights
    for j in range(len(goodroutes[i])):"""



'''

#We need a list of all the types of planes so that we can find out how many people each can carry
#Each entry of planes.dat.txt contains three things: the name, the IATA code, and the ICAO code
#We need the latter two

types=[]
for i in range(len(planes)):
    if planes[i][1:] not in types:
        types.append(planes[i][1:])

#types.sort()
#for i in range(len(types)):
#    print(types[i][0]+str(', ')+types[i][1])
    
#There are 246 types of planes
#Let's try just the IATA codes

IATA=[]
for i in range(len(planes)):
    if planes[i][1] not in IATA:
        IATA.append(planes[i][1])

IATA.sort()
for i in range(len(IATA)):
    print(IATA[i])

'''