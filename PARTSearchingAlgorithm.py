
# CREATE A SEARCHING ALGORITHM FOR PLANE

import numpy as np
import math
from matplotlib import pyplot as plt
from matplotlib import animation


# ---------------------------------------------------------
# plot points
# ---------------------------------------------------------

# import points
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


    

# create figure and axis
fig, ax = plt.subplots()
xdata, ydata = [], []
ln, = plt.plot([], [], 'ro')

# axis boundaries on grid
minX = 90
maxX = -90
minY = 180
maxY = -180


for pt in searchGridPoints :
    xvalue = pt["latitude"]
    yvalue = pt["longitude"]
    xdata.append(xvalue)
    ydata.append(yvalue)
    
    # find maximum and minimum values
    if (xvalue > maxX):
        maxX = xvalue
    if (xvalue < minX):
        minX = xvalue
    if (yvalue > maxY):
        maxY = yvalue
    if (yvalue < minY):
        minY = yvalue


lengthx = maxX - minX
lengthy = maxY - minY
# initialize background frame
def init():
    ax.set_xlim(minX - lengthx * 0.2, maxX + lengthx * 0.2)
    ax.set_ylim(minY - lengthy * 0.2, maxY + lengthy * 0.2)
    ax.plot(xdata, ydata, 'b')
    ax.set_aspect('equal')
    ax.set_xlabel("latitude")
    ax.set_ylabel("longitude")
    createPts()
    return ln,

# update function
def update(frame):
    global prevPlanePts, prevCamPts, prevConnectorPts, planeAngle
    
    
    planeAngle %= 2 * math.pi
    if (planeAngle < 0):
        planeAngle += 2 * math.pi

    # commands, implement algorithm here
    moveToPts(pts)
    
    # remove previous points for visual clarity
    if (frame > 0):
        prevPlanePts.remove()
        prevCamPts.remove()
        #prevConnectorPts.remove()
    prevPlanePts, = ax.plot(planePosX, planePosY, marker = (3, 0, 30+planeAngle*180/math.pi), markersize = 12, color='green') # plot plane
    ax.plot(cameraPosX, cameraPosY, 'yo') # plot searched points
    #prevConnectorPts, = ax.plot([planePosX, cameraPosX], [planePosY, cameraPosY], color = 'black', linewidth = 3) # connect plane and camera
    prevCamPts, = ax.plot(cameraPosX, cameraPosY, 'mo') # plot camera current position
    
    #ax.plot(minX + frame * lengthx / 10, minY + frame * lengthy / 10, 'go')
    ln.set_data(xdata, ydata)
    return ln,

# CONSTANTS - ENTER VALUES FOR THESE DEPENDING ON PROPERTIES OF PLANE/CAMERA
planeRadius = 0.002
cameraRadius = 0.002
distToCamera = 0.0008
planeSpeed = 0.0001
# variables for properties of the plane and the camera
planePosX = (maxX + minX) / 2
planePosY = (maxY + minY) / 2
planeAngle = 0
planeAngleSpeed = math.pi / 40
cameraPosX = planePosX + distToCamera * math.cos(planeAngle)
cameraPosY = planePosY + distToCamera * math.sin(planeAngle)
curPt = 0
pts = []

def moveForward():
    global planePosX
    global planePosY
    planePosX += planeSpeed * math.cos(planeAngle)
    planePosY += planeSpeed * math.sin(planeAngle)
    setCamera()

def turn(turnby):
    global planeAngle
    planeAngle += turnby
    setCamera()

def setCamera():
    global cameraPosX
    global cameraPosY
    cameraPosX = planePosX + distToCamera * math.cos(planeAngle)
    cameraPosY = planePosY + distToCamera * math.sin(planeAngle)
    
def turnTo(x, y):
    global planeAngle, planePosX, planePosY
    if (math.fabs(x - planePosX) <= 0.01):
        if (y - planePosY < 0):
            difX = 0.001
        else:
            difX = -0.001
    else:
        difX = x - planePosX
    if (math.fabs(y - planePosY) <= 0.01):
        if (x - planePosX < 0):
            difY = 0.001
        else:
            difY = -0.001
    else:
        difY = y - planePosY
    targetAngle = math.atan((difY) / (difX))
    targetAngle += (difX < 0) * math.pi
    '''
    difX = x - planePosX
    difY = y - planePosY
    if (math.fabs(difX) <= 0.01):
        if (difY > 0):
            targetAngle = math.pi / 2
        else:
            targetAngle = math.pi * 3 / 2
    elif (math.fabs(difY) <= 0.01):
        if (difX > 0):
            targetAngle = 0
        else:
            targetAngle = math.pi
    else:
        targetAngle = math.atan((y - planePosY) / (difX))
        targetAngle += (difX < 0) * math.pi
    
    '''
    if (planeAngle > targetAngle):
        turn(-planeAngleSpeed)
    elif (planeAngle <= targetAngle):
        turn(planeAngleSpeed)
    setCamera()
    
def moveTo(x, y):
    
    if (math.sqrt((planePosX - x) ** 2 + (planePosY - y) ** 2) > planeSpeed * 5):
        moveForward()
    
    
    return True
    #=--------------
    if (math.fabs(x - planePosX) <= 0.01):
        if (y - planePosY < 0):
            difX = 0.001
        else:
            difX = -0.001
    else:
        difX = x - planePosX
    if (math.fabs(y - planePosY) <= 0.01):
        if (x - planePosX < 0):
            difY = 0.001
        else:
            difY = -0.001
    else:
        difY = y - planePosY
    targetAngle = math.atan((difY) / (difX))
    targetAngle += (difX < 0) * math.pi
   
    if (math.fabs(targetAngle - planeAngle) > planeAngleSpeed * 2 and math.sqrt((planePosX - x) ** 2 + (planePosY - y) ** 2) > planeSpeed * 5):
        turnTo(x, y)
        setCamera()
        return False
    
    if (math.sqrt((planePosX - x) ** 2 + (planePosY - y) ** 2) > planeSpeed * 5):
        moveForward()
        setCamera()
        return False
    
    return True
        
    

def moveToPts(pts):
    global curPt
    if (curPt < len(pts) and moveTo(pts[curPt][0], pts[curPt][1])) :
        curPt += 1
    setCamera()

def createPts():
    global pts
    pts = []
    for pt in searchGridPoints:
        pts.append([pt["latitude"], pt["longitude"]])
    #pts = [[minX, minY], [minX, maxY], [maxX, maxY], [maxX, minY]]
    return pts

   





# animate
ani = animation.FuncAnimation(fig, update, frames=np.linspace(0, 4*np.pi, 100), init_func = init, blit=True)
plt.show()

writergif = animation.PillowWriter(fps=30)
ani.save('PARTSearchAlgorithmVersion2.gif',writer=writergif)

# ---------------------------------------------------------
# create animation
# ---------------------------------------------------------

# ---------------------------------------------------------
# draw circle
# ---------------------------------------------------------


# ---------------------------------------------------------
# determine whether points have been searched or not while flying
# ---------------------------------------------------------