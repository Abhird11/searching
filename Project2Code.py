
import math
import matplotlib.pyplot as plt

# Hard Coded
eOut = 120
g = 9.81
densityWater = 1000

# inputs

pumpEfficiency = 0.9
pumpFlowVolume = 65
pipeDiameter = 2
pipeLength = 75
pipeFriction = 0.05
reservoirDepth = 10
reservoirElevation = 50
bendCoefficient1 = 0.15
bendCoefficient2 = 0.2
turbineEfficiency = 0.92
turbineFlowVolume = 30

# intermediate variables
pipeArea = (pipeDiameter / 2) ** 2 * math.pi
velocityUp = pumpFlowVolume / pipeArea
velocityDown = turbineFlowVolume / pipeArea
effectiveElevation = reservoirElevation + reservoirDepth / 2
eOutJoules = eOut * (3.6 * math.pow(10, 9))

mass = densityWater * pipeArea * velocityUp * 7.5 #WRONG





print(str(mass))

def reservoirArea():
    return 1

def energyIn():
    return 1

def efficiency():
    return 1

def timeToFill():
    return 1

def timeToEmpty():
    return 1

def cost():
    return 1