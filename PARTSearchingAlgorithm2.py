import math
import matplotlib.pyplot as plt
import json
import random

random.seed(3)

# REMAINING TASKS
#
# *** CONVERT EVERYTHING TO METERS ***
# * Find way to reconvert back into latitude and longitude for output file
# * Find scale of stationary obstacle points' radius, plot stationary obstacles points correctly and to scale
# * Add logic to determine if a certain point is on a stationary obstacle
# * Add logic to change way points from the obstacle to just outside the obstacle
# * Account for altitude, make radius of camera change as altitude changes
#
# NOT SO IMPORTANT, DO AT END IF TIME/EFFORT PERMITS
#
# find a way to save efficiency in the middle of the boundary points

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
lonMultiplier = 111139 * math.cos(math.cos(minLon) * math.pi / 180)
latMultiplier = 111120
maxX = (maxLat - minLat) * lonMultiplier
maxY = (maxLon - minLon) * latMultiplier
obstacleRadiusConversion = 0.00013
obstacleHeightConversion = 1
        
print("Length (longitude): " + str(maxX))
print("Width (latitude): " + str(maxY))


meterSearchGridPoints = []
meterStationaryObstacles = []

for i in searchGridPoints:
    meterSearchGridPoints.append({"latitude" : i["latitude"] * latMultiplier, "longitude" : i["longitude"] * lonMultiplier})

for i in stationaryObstacles:
    meterStationaryObstacles.append({"latitude" : i["latitude"] * latMultiplier, "radius" : i["radius"] * obstacleRadiusConversion, "longitude" : i["longitude"] * lonMultiplier, "height" : i["height"] * obstacleHeightConversion})

# variables to edit based on the physical plane
cameraWidth = 8
startPosX = minLat + (random.random() * (maxLat - minLat))#minX + (random.random() * (maxX - minX))
startPosY = minLon + (random.random() * (maxLon - minLon))#minY + (random.random() * (maxY - minY))
startAlt = 200

#programming variables to change


changeInX = cameraWidth / 17391.3

xWayPts = [startPosX]
yWayPts = [startPosY]
altWayPts = [startAlt]

for i in range(len(searchGridPoints)):
    dist = math.sqrt(math.pow(searchGridPoints[i]["latitude"] - startPosX, 2) + math.pow(searchGridPoints[i]["longitude"] - startPosY, 2))
    if (dist < minDist):
        minDist = dist
        minDistInd = i

searchGridPoints.pop()
for i in range(minDistInd):
    searchGridPoints.append(searchGridPoints[0])
    searchGridPoints.pop(0)
searchGridPoints.append(searchGridPoints[0])
    


def calcAngle(x1, y1, x2, y2):
    slope = (y2 - y1) / (x2 - x1)
    
    ang = math.atan(slope)
    
    
    if (x2 < x1):
        ang += math.pi
    elif (math.fabs(x1 - x2) < 0.000001 and y2 < y1):
        ang += math.pi
    
    
    ang %= 2 * math.pi
    
    return round(ang, 3)
    
def getAngle(x, y, x1, y1, x2, y2):
    angleLine1 = calcAngle(x, y, x1, y1)
    angleLine2 = calcAngle(x, y, x2, y2)
    
    
    
    
    angle1 = ((angleLine1 + angleLine2) / 2) % (2 * math.pi)
    angle2 = (angle1 + math.pi) % (2 * math.pi)
    
    angle = angle1
    
    if (angleLine2 < angle1 < angleLine1):
        angle = angle1
    else:
        angle = angle2
    
    return angle
    
def inObstacle(x, y):
    obInd = -1
    for i in range(len(stationaryObstacles)):
        obX = stationaryObstacles[i]["latitude"]
        obY = stationaryObstacles[i]["longitude"]
        obRad = stationaryObstacles[i]["radius"]
        
        if (math.sqrt(math.pow(x - obX, 2) + math.pow(y - obY), 2) < obRad):
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
        while (curX <= maxX):
            xWayPts.append(curX)
            yWayPts.append(curY)
            altWayPts.append(200)
            if (curChange == 1):
                curY = maxY
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
        pt1x = searchGridPoints[-2]["latitude"]
        pt2x = searchGridPoints[1]["latitude"]
        pt1y = searchGridPoints[-2]["longitude"]
        pt2y = searchGridPoints[1]["longitude"]
        ptx = searchGridPoints[0]["latitude"]
        pty = searchGridPoints[0]["longitude"]
        
        
        angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        curXPts = []
        curYPts = []
        
        for i in range(1, len(searchGridPoints) - 1):
            pt1x = searchGridPoints[i-1]["latitude"]
            pt2x = searchGridPoints[i+1]["latitude"]
            pt1y = searchGridPoints[i-1]["longitude"]
            pt2y = searchGridPoints[i+1]["longitude"]
            ptx = searchGridPoints[i]["latitude"]
            pty = searchGridPoints[i]["longitude"]
            
            angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        pt1x = searchGridPoints[-2]["latitude"]
        pt2x = searchGridPoints[1]["latitude"]
        pt1y = searchGridPoints[-2]["longitude"]
        pt2y = searchGridPoints[1]["longitude"]
        ptx = searchGridPoints[0]["latitude"]
        pty = searchGridPoints[0]["longitude"]
        
        angles.append(getAngle(ptx, pty, pt1x, pt1y, pt2x, pt2y))
        
        for i in range(len(angles)):
            curXPts.append(searchGridPoints[i]["latitude"])
            curYPts.append(searchGridPoints[i]["longitude"])
            
        for i in range(6):
            for i in range(len(angles)):
                xWayPts.append(curXPts[i] + cameraWidth / 26666.666 * math.cos(angles[i]))
                yWayPts.append(curYPts[i] + cameraWidth / 26666.666 * math.sin(angles[i]))
                curXPts[i] = curXPts[i] + cameraWidth / 26666.666 * math.cos(angles[i])
                curYPts[i] = curYPts[i] + cameraWidth / 26666.666 * math.sin(angles[i])
                altWayPts.append(200)

        
            
              
createPoints(2)
wayPts = []
for i in range(len(xWayPts)):
    wayPts.append({"latitude" : xWayPts[i], "longitude" : yWayPts[i], "altitude" : altWayPts[i]})
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
        for pt in searchGridPoints:
            centerX += pt["latitude"]
            centerY += pt["longitude"]
        centerX /= len(searchGridPoints)
        centerY /= len(searchGridPoints)
        
        # find closest and longest distances to boundary points
        minDist = 99999
        maxDist = 0
        data = []
        for i in range(len(searchGridPoints) - 1):
            dist = math.sqrt((startPosX - searchGridPoints[i]["latitude"]) ** 2 + (startPosY - searchGridPoints[i]["longitude"]) ** 2)
            if (dist > maxDist):
                maxDist = dist
                maxPt = i
            elif (dist < minDist):
                minDist = dist
                minPt = i
        
        curPt = 1
        print(minPt)
        for i in range(minPt, len(searchGridPoints) - 1):
            dist = math.sqrt((centerX - searchGridPoints[i]["latitude"]) ** 2 + (centerY - searchGridPoints[i]["longitude"]) ** 2)
            slope = (centerY - searchGridPoints[i]["longitude"]) / (centerX - searchGridPoints[i]["latitude"])
            data.append({"number" : curPt, "distance" : dist, "slope" : slope})
            curPt += 1
            
        for i in range(1, minPt):
            dist = math.sqrt((centerX - searchGridPoints[i]["latitude"]) ** 2 + (centerY - searchGridPoints[i]["longitude"]) ** 2)
            slope = (centerY - searchGridPoints[i]["longitude"]) / (centerX - searchGridPoints[i]["latitude"])
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


for pt in searchGridPoints:
    xGridPts.append(pt["latitude"])
    yGridPts.append(pt["longitude"])
    



plt.plot(xWayPts, yWayPts, color = "orange", marker = "o", markerfacecolor = "green", markeredgecolor = "green", lineWidth = cameraWidth, markersize = 3) #area
plt.plot(xWayPts, yWayPts, color = "black", lineWidth = 1)
plt.plot(xGridPts, yGridPts, color = "blue", linewidth = 3)
for i in range(len(xGridPts)):
    plt.text(xGridPts[i], yGridPts[i], "B" + str(i))
for i in range(len(stationaryObstacles)):
    plt.scatter([stationaryObstacles[i]["latitude"]], [stationaryObstacles[i]["longitude"]], s=(576 * stationaryObstacles[i]["radius"] * obstacleRadiusConversion) ** 2, c = "yellow", zorder = 3)
    plt.text(stationaryObstacles[i]["latitude"], stationaryObstacles[i]["longitude"], "O" + str(i))
plt.gca().set_aspect('equal', adjustable = 'box')
plt.grid()
