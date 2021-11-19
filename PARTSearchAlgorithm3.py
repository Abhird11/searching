import math
import matplotlib.pyplot as plt
import json
import random

#random.seed(3)

# REMAINING TASKS
#
# * Account for altitude, make radius of camera change as altitude changes
# * Account for location of UGV
#
# NOT SO IMPORTANT, DO AT END IF TIME/EFFORT PERMITS
#
# find a way to save efficiency in the middle of the boundary points
#
# LATER ON MORE COMPLEX TASKS
# * Try to think of a way to not search around an obstacle twice
# * Try to think of a way to prioritize certain regions that have a higher chance of containing targets mid-flight (this will likely be another program)

numLoops = 7
cameraWidth = 100

# import boundary points
searchGridPoints = [{
            "latitude": 38.1444444444444,
            "longitude": -76.4280916666667
        },
        {
            "latitude": 38.1459444444444,
            "longitude": -76.4237944444445
        },
        {
            "latitude": 38.1439305555556,
            "longitude": -76.4227444444444
        },
        {
            "latitude": 38.1417138888889,
            "longitude": -76.4253805555556
        },
        {
            "latitude": 38.1412111111111,
            "longitude": -76.4322361111111
        },
        {
            "latitude": 38.1431055555556,
            "longitude": -76.4335972222222
        },
        {
            "latitude": 38.1441805555556,
            "longitude": -76.4320111111111
        },
        {
            "latitude": 38.1452611111111,
            "longitude": -76.4289194444444
        },
        {
            "latitude": 38.1444444444444,
            "longitude": -76.4280916666667
        }
    ]

#import obstacle points
stationaryObstacles = [{
            "latitude": 38.146689,
            "radius": 150.0,
            "longitude": -76.426475,
            "height": 750.0
        },
        {
            "latitude": 38.142914,
            "radius": 300.0,
            "longitude": -76.430297,
            "height": 300.0
        },
        {
            "latitude": 38.149504,
            "radius": 100.0,
            "longitude": -76.43311,
            "height": 750.0
        },
        {
            "latitude": 38.148711,
            "radius": 300.0,
            "longitude": -76.429061,
            "height": 750.0
        },
        {
            "latitude": 38.144203,
            "radius": 50.0,
            "longitude": -76.426155,
            "height": 400.0
        },
        {
            "latitude": 38.146003,
            "radius": 225.0,
            "longitude": -76.430733,
            "height": 500.0
        },
        {
            "latitude": 38.147,
            "radius": 100.0,
            "longitude": -76.429,
            "height": 500.0
        }
    ]



# create waypoints
minLat = 10000
maxLat = -10000
minLon = 10000
maxLon = -10000
minDist = 999999
minDistInd = 0


# FUNCTIONS FROM LEONARD
def calc_bearing(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2- lon1
    return math.atan2(math.sin(dlon) * math.cos(lat2), math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon))

def calc_haversine(lat1, lon1, lat2, lon2):
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)
    dlat = lat2 - lat1
    dlon = lon2- lon1
    a = pow(math.sin(dlat / 2),2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin(dlon / 2), 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = 6371e3 * c  * 3.28084 #  feet
    return d

def cartesian_to_decimal(x, y, lat1, lon1):
    bearing = math.atan(y / x)
    d = x / math.cos(bearing)
    r = 6371e3 * 3.28084 # feet
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.degrees(math.asin(math.sin(lat1) * math.cos(d / r) +
                        math.cos(lat1) * math.sin(d / r) * math.cos(bearing)))
    lon2 =  math.degrees(lon1 + math.atan2(math.sin(bearing) * math.sin(d / r) * math.cos(lat1),
                                math.cos(d / r) - math.sin(lat1) * math.sin(math.radians(lat2))))
    return lat2, lon2



def decimal_to_cartesian(lat1, lon1, lat2, lon2):
    d = calc_haversine(lat2, lon2, lat1, lon1)
    bearing = calc_bearing(lat2, lon2, lat1, lon1)
    x = d * math.cos(bearing)
    y = d * math.sin(bearing)
    return x, y

# END OF FUNCTIONS FROM LEONARD

for pt in searchGridPoints:
    if (pt["latitude"] < minLat):
        minLat = pt["latitude"]
    if (pt["latitude"] > maxLat):
        maxLat = pt["latitude"]
    if (pt["longitude"] > maxLon):
        maxLon = pt["longitude"]
    if (pt["longitude"] < minLon):
        minLon = pt["longitude"]

minX = 0
minY = 0
maxYSearch, maxXSearch = decimal_to_cartesian(maxLat, maxLon, minLat, minLon)
        


feetSearchGridPoints = []
feetStationaryObstacles = []

for i in searchGridPoints:
    curLat, curLon = decimal_to_cartesian(i["latitude"], i["longitude"], minLat, minLon)
    feetSearchGridPoints.append({"latitude" : curLat, "longitude" : curLon})

for i in stationaryObstacles:
    curLat, curLon = decimal_to_cartesian(i["latitude"], i["longitude"], minLat, minLon)
    feetStationaryObstacles.append({"latitude" : curLat, "radius" : i["radius"], "longitude" : curLon, "height" : i["height"]})

feetStationaryObstacles.append({"latitude" : 900, "radius" : 150, "longitude" : 1500, "height" : 50})

'''
feetStationaryObstacles = [{
    "latitude" : 2000,
    "radius" : 500,
    "longitude" : 2000,
    "height" : 50
    },
    {
    "latitude": 3000,
    "radius" : 5,
    "longitude" : 2000,
    "height" : 50
     }
     ]
'''
maxXGrid = maxXSearch
maxYGrid = maxYSearch
minXGrid = 0
minYGrid = 0

for i in feetStationaryObstacles:
    if (i["latitude"] + i["radius"] > maxYGrid):
        maxYGrid = i["latitude"] + i["radius"]
    if (i["longitude"] + i["radius"] > maxXGrid):
        maxXGrid = i["longitude"] + i["radius"]
    if (i["latitude"] - i["radius"] < minYGrid):
        minYGrid = i["latitude"] - i["radius"]
    if (i["longitude"] - i["radius"] < minXGrid):
        minXGrid = i["longitude"] - i["radius"]

gridLength = maxXGrid - minXGrid
gridHeight = maxYGrid - minYGrid
minXGrid = -0.1 * gridLength
maxXGrid = gridLength * 1.1
minYGrid = -0.1 * gridHeight
maxYGrid = gridHeight * 1.1
gridLength = maxXGrid - minXGrid
gridHeight = maxYGrid - minYGrid

# variables to edit based on the physical plane

startPosX = minX + (random.random() * (maxXSearch - minX))
startPosY = minY + (random.random() * (maxYSearch - minY))
startAlt = 200

#programming variables to change


changeInX = cameraWidth / 17391.3

xWayPts = [startPosX]
yWayPts = [startPosY]
altWayPts = [startAlt]

for i in range(len(feetSearchGridPoints)):
    dist = math.sqrt(math.pow(feetSearchGridPoints[i]["longitude"] - startPosX, 2) + math.pow(feetSearchGridPoints[i]["latitude"] - startPosY, 2))
    if (dist < minDist):
        minDist = dist
        minDistInd = i

feetSearchGridPoints.pop()
for i in range(minDistInd):
    feetSearchGridPoints.append(feetSearchGridPoints[0])
    feetSearchGridPoints.pop(0)
feetSearchGridPoints.append(feetSearchGridPoints[0])
    

def calcAngle(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    
    ang = math.atan(slope)
    
    
    if (x2 < x1):
        ang += math.pi
    elif (math.fabs(x1 - x2) < 0.0000001 and y2 < y1):
        ang += math.pi
    
    
    ang %= 2 * math.pi
    
    return round(ang, 3)
    
def getAngle(x, y, x1, y1, x2, y2):
    angleLine1 = calcAngle(x, y, x1, y1)
    angleLine2 = calcAngle(x, y, x2, y2)
    
    
    
    
    angle1 = ((angleLine1 + angleLine2) / 2) % (2 * math.pi)
    angle2 = (angle1 + math.pi) % (2 * math.pi)
    
    angle = angle1
    
    if (angleLine2 > angle1 and angle1 > angleLine1):
        angle = angle1
    else:
        angle = angle2
    
    return angle
    
def inObstacle(x, y):
    obInd = -1
    for i in range(len(feetStationaryObstacles)):
        obX = feetStationaryObstacles[i]["longitude"]
        obY = feetStationaryObstacles[i]["latitude"]
        obRad = feetStationaryObstacles[i]["radius"]
        
        if (math.sqrt(math.pow(x - obX, 2) + math.pow(y - obY, 2)) < obRad):
            obInd = i
    
    return obInd
        

# FUNCTION TO CREATE WAYPOINTS
# MODE 1 -- basic go up and down
# MODE 2 -- more efficient, go around boundary
def createPoints(mode):
    if (mode == 1):
        curX = minX
        curY = minY
        curChange = 1
        while (curX <= maxXSearch):
            xWayPts.append(curX)
            yWayPts.append(curY)
            altWayPts.append(200)
            if (curChange == 1):
                curY = maxYSearch
                curChange = 2
            elif (curChange == 2):
                curX += changeInX
                curChange = 3
            elif (curChange == 3):
                curY = minY
                curChange = 4
            elif (curChange == 4):
                curX += changeInX
                curChange = 1
                
    elif (mode == 2):
        angles = []
        pt1y = feetSearchGridPoints[-2]["latitude"]
        pt2y = feetSearchGridPoints[1]["latitude"]
        pt1x = feetSearchGridPoints[-2]["longitude"]
        pt2x = feetSearchGridPoints[1]["longitude"]
        pty = feetSearchGridPoints[0]["latitude"]
        ptx = feetSearchGridPoints[0]["longitude"]
        
        
        angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        curXPts = []
        curYPts = []
        
        for i in range(1, len(feetSearchGridPoints) - 1):
            pt1y = feetSearchGridPoints[i-1]["latitude"]
            pt2y = feetSearchGridPoints[i+1]["latitude"]
            pt1x = feetSearchGridPoints[i-1]["longitude"]
            pt2x = feetSearchGridPoints[i+1]["longitude"]
            pty = feetSearchGridPoints[i]["latitude"]
            ptx = feetSearchGridPoints[i]["longitude"]
            
            angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        pt1y = feetSearchGridPoints[-2]["latitude"]
        pt2y = feetSearchGridPoints[1]["latitude"]
        pt1x = feetSearchGridPoints[-2]["longitude"]
        pt2x = feetSearchGridPoints[1]["longitude"]
        pty = feetSearchGridPoints[0]["latitude"]
        ptx = feetSearchGridPoints[0]["longitude"]
        
        angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        for i in range(len(angles)):
            curYPts.append(feetSearchGridPoints[i]["latitude"] - 1/2 * cameraWidth * math.sin(angles[i]))
            curXPts.append(feetSearchGridPoints[i]["longitude"] - 1/2 * cameraWidth * math.cos(angles[i]))
            
        for i in range(numLoops):
            for i in range(len(angles)):
                if (inObstacle(curXPts[i] + cameraWidth * math.cos(angles[i]), curYPts[i] + cameraWidth * math.sin(angles[i])) == -1):
                    xWayPts.append(curXPts[i] + cameraWidth * math.cos(angles[i]))
                    yWayPts.append(curYPts[i] + cameraWidth * math.sin(angles[i]))
                else:
                    angleToPrev = calcAngle(curXPts[i] + cameraWidth * math.cos(angles[i]), curYPts[i] + cameraWidth * math.sin(angles[i]), curXPts[i-1], curYPts[i-1])
                    
                    adder = cameraWidth
                    testPtX = curXPts[i] + cameraWidth * math.cos(angles[i]) + adder * math.cos(angleToPrev)
                    testPtY = curYPts[i] + cameraWidth * math.sin(angles[i]) + adder * math.sin(angleToPrev)
                    
                    while (inObstacle(testPtX, testPtY) != -1):
                        testPtX += adder * math.cos(angleToPrev)
                        testPtY += adder * math.sin(angleToPrev)
                    
                    #testPtX += adder * math.cos(angleToPrev)
                    #testPtY += adder * math.sin(angleToPrev)
                    
                    xWayPts.append(testPtX)
                    yWayPts.append(testPtY)
                    
                    angleToNext = calcAngle(curXPts[i] + cameraWidth * math.cos(angles[i]), curYPts[i] + cameraWidth * math.sin(angles[i]), curXPts[(i + 1) % len(curXPts)] + cameraWidth * math.cos(angles[(i+1)%len(angles)]), curYPts[(i+1)%len(curYPts)] + cameraWidth * math.sin(angles[(i+1)%len(angles)]))
                    
                    testPtX = curXPts[i] + cameraWidth * math.cos(angles[i]) + adder * math.cos(angleToNext)
                    testPtY = curYPts[i] + cameraWidth * math.sin(angles[i]) + adder * math.sin(angleToNext)
                    
                    while (inObstacle(testPtX, testPtY) != -1):
                        testPtX += adder * math.cos(angleToNext)
                        testPtY += adder * math.sin(angleToNext)
                    
                    #testPtX += adder * math.cos(angleToNext)
                    #testPtY += adder * math.sin(angleToNext)
                    
                    xWayPts.append(testPtX)
                    yWayPts.append(testPtY)
                    altWayPts.append(200)
                    
                    # NEXT SESSION: WORK ON CODE TO MAKE NEW WAY POINTS BE AROUND OBSTACLES
                    
                curXPts[i] = curXPts[i] + cameraWidth * math.cos(angles[i])
                curYPts[i] = curYPts[i] + cameraWidth * math.sin(angles[i])
                altWayPts.append(200)

        
            
              
createPoints(2)
wayPts = []

for i in range(len(xWayPts)):
    curLatX, curLonX = cartesian_to_decimal(xWayPts[i], yWayPts[i], minLat, minLon)
    wayPts.append({"latitude" : curLatX, "longitude" : curLonX, "altitude" : altWayPts[i]})
# FUNCTION TO CREATE WAYPOINTS
# MODE 1 --- basic go up and down
# MODE 2 --- go from each boundary point
'''
def createPoints(mode):
    if (mode == 1):
        for i in range(len(xWayPts)):
            wayPts.append({"latitude" : xWayPts[i], "longitude" : yWayPts[i], "altitude" : 200})
    if (mode == 2):
        # calculate center of boundary points
        centerX = 0;
        centerY = 0;
        for pt in meterSearchGridPoints:
            centerX += pt["latitude"]
            centerY += pt["longitude"]
        centerX /= len(meterSearchGridPoints)
        centerY /= len(meterSearchGridPoints)
        
        # find closest and longest distances to boundary points
        minDist = 99999
        maxDist = 0
        data = []
        for i in range(len(meterSearchGridPoints) - 1):
            dist = math.sqrt((startPosX - meterSearchGridPoints[i]["latitude"]) ** 2 + (startPosY - meterSearchGridPoints[i]["longitude"]) ** 2)
            if (dist > maxDist):
                maxDist = dist
                maxPt = i
            elif (dist < minDist):
                minDist = dist
                minPt = i
        
        curPt = 1
        print(minPt)
        for i in range(minPt, len(meterSearchGridPoints) - 1):
            dist = math.sqrt((centerX - meterSearchGridPoints[i]["latitude"]) ** 2 + (centerY - meterSearchGridPoints[i]["longitude"]) ** 2)
            slope = (centerY - meterSearchGridPoints[i]["longitude"]) / (centerX - meterSearchGridPoints[i]["latitude"])
            data.append({"number" : curPt, "distance" : dist, "slope" : slope})
            curPt += 1
            
        for i in range(1, minPt):
            dist = math.sqrt((centerX - meterSearchGridPoints[i]["latitude"]) ** 2 + (centerY - meterSearchGridPoints[i]["longitude"]) ** 2)
            slope = (centerY - meterSearchGridPoints[i]["longitude"]) / (centerX - meterSearchGridPoints[i]["latitude"])
            data.append({"number" : curPt, "distance" : dist, "slope" : slope})
            curPt += 1
            
        
        
        print(data)
        
        
        '''
                


# output to json
filepath = "searchpath.json"
with open(filepath, "w") as file:
    json.dump(wayPts, file)


# boundary points
xGridPts = []
yGridPts = []

# obstacle points


for pt in feetSearchGridPoints:
    yGridPts.append(pt["latitude"])
    xGridPts.append(pt["longitude"])
    
for i in range(len(xWayPts)):
    x = xWayPts[i]
    y = yWayPts[i]

print(str(minXGrid), str(minYGrid))

plt.figure(figsize = [5, 5])
ax = plt.axes([0.1, 0.1, 0.8, 0.8], xlim=(minXGrid, maxXGrid), ylim=(minYGrid, maxYGrid))
plt.plot(xWayPts, yWayPts, color = "orange", marker = "o", markerfacecolor = "green", markeredgecolor = "green", lineWidth = cameraWidth / gridLength * 5 * 0.8 * 72, markersize = 3) #area
plt.plot(xWayPts, yWayPts, color = "black", lineWidth = 1)
plt.plot(xGridPts, yGridPts, color = "blue", linewidth = 3)


for i in range(len(xGridPts)):
    plt.text(xGridPts[i], yGridPts[i], "B" + str(i))
for i in range(len(feetStationaryObstacles)):
    ax.scatter([feetStationaryObstacles[i]["longitude"]], [feetStationaryObstacles[i]["latitude"]], s=(2 * feetStationaryObstacles[i]["radius"] / gridLength * 5 * 0.8 * 72) ** 2, c = "yellow", zorder = 3)
    plt.text(feetStationaryObstacles[i]["longitude"], feetStationaryObstacles[i]["latitude"], "O" + str(i))
plt.gca().set_aspect('equal', adjustable = 'box')
plt.xlabel("Horizontal (feet)")
plt.ylabel("Vertical (feet)")
plt.title("Map of boundary points, obstacles, and path")
plt.grid()
plt.show()

for i in range(len(xWayPts)):
    if (not inObstacle(xWayPts[i], yWayPts[i])):
        print("Error: point " + str(i) + " in obstacle " + str(inObstacle(xWayPts[i], yWayPts[i])))