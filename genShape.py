# Test Shape Display

# STIM RECT ISNT WORKING, WANT TO MAKE THIS RUN MORE LOGICALLY, RN ITS SHIT
from __future__ import division
from psychopy import visual, event, core
from psychopy.visual import ShapeStim 
import random
import math
import pickle
import numpy
import pylab



# Which stim to display
# true if rectangles, false if cubes
rectangles = False

numRect = 4
numCube = 1



# 300 x 4 x 2 matrix 
# 300 entries, 4 shapes, xy for each shape
f = open('genCoor.pckl', 'rb')
genCoor = pickle.load(f)
f.close()
win = visual.Window([1600, 900], units = 'height', fullscr=True)
# allowGUI=False, waitBlanking=True,
# win = visual.Window(size=(500, 400), units='height')

clock = core.Clock()
recLength  = .09
recWidth   = .27
cubeLength = .15
cubeWidth  = .15

shapeVert  = numpy.zeros((4,4,4,2))
cubeVert   = numpy.zeros((numCube,3,4,2))
cubeOne    = numpy.zeros((numCube,3,4,2))
cubeTwo    = numpy.zeros((numCube,3,4,2))

stimOne    = [0,0]
stimTwo    = [0,0]
stimThree  = [0,0]
stimFour   = [0,0]
stimRect   = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

stimOneCube    = [[0,0,0],[0,0,0]]
stimTwoCube    = [[0,0,0],[0,0,0]]

colorIndexs = [0,0,0,0,0,0,0,0]
firstColors = ['blue','red','blue','red']
random.shuffle(firstColors)
secondColors = [0,0,0,0]

# takes vertical rectangle and rotates by 45 degrees each loop creating 4 different orientations
def rectangleCreation(n,rotN):
    for k in range(0,rotN):
        center = [shapes[k][0], shapes[k][1]]
        p1 = [center[0]-recWidth, center[1]-recLength]
        p2 = [center[0]-recWidth, center[1]+recLength]
        p3 = [center[0]+recWidth, center[1]+recLength]
        p4 = [center[0]+recWidth, center[1]-recLength]
        shapeVert[k][n] = rotate(numpy.array([p1, p2, p3, p4]),center,math.pi*k/4)
    return shapeVert

    
# creates three-sided cubes
def cubeOneCreation(n):
    for k in range(0,2):
        center = [shapes[k][0], shapes[k][1]]
        p1 = [center[0]          , center[1]]
        p2 = [center[0]          , center[1]-cubeLength]
        p3 = [center[0]-cubeWidth, center[1]-cubeLength/2]
        p4 = [center[0]-cubeWidth, center[1]+cubeLength/2]
        sideOne = [p1, p2, p3, p4]
        
        q1 = [center[0]          , center[1]]
        q2 = [center[0]          , center[1]-cubeLength]
        q3 = [center[0]+cubeWidth, center[1]-cubeLength/2]
        q4 = [center[0]+cubeWidth, center[1]+cubeLength/2]
        sideTwo = [q1, q2, q3, q4]
        
        r1 = [center[0]          , center[1]]
        r2 = [center[0]-cubeWidth, center[1]+cubeLength/2]
        r3 = [center[0]          , center[1]+cubeLength]
        r4 = [center[0]+cubeWidth, center[1]+cubeLength/2]
        sideThree = [r1, r2, r3, r4]
        # k cubes x 3 sides x 4 vertices x 2 coordinates
        cubeOne[k] = numpy.array([sideOne, sideTwo, sideThree])
    return cubeOne

def cubeTwoCreation(n):
    for k in range(2,4):
        center = [shapes[k][0], shapes[k][1]]
        p1 = [center[0]          , center[1]]
        p2 = [center[0]          , center[1]+cubeLength]
        p3 = [center[0]+cubeWidth, center[1]+cubeLength/2]
        p4 = [center[0]+cubeWidth, center[1]-cubeLength/2]
        sideOne = [p1, p2, p3, p4]
        
        q1 = [center[0]          , center[1]]
        q2 = [center[0]          , center[1]+cubeLength]
        q3 = [center[0]-cubeWidth, center[1]+cubeLength/2]
        q4 = [center[0]-cubeWidth, center[1]-cubeLength/2]
        sideTwo = [q1, q2, q3, q4]
        
        r1 = [center[0]          , center[1]]
        r2 = [center[0]-cubeWidth, center[1]-cubeLength/2]
        r3 = [center[0]          , center[1]-cubeLength]
        r4 = [center[0]+cubeWidth, center[1]-cubeLength/2]
        sideThree = [r1, r2, r3, r4]
        # k cubes x 3 sides x 4 vertices x 2 coordinates
        cubeTwo[k-2] = numpy.array([sideOne, sideTwo, sideThree])
    return cubeTwo


# randomizes color order, makes sure same two shapes dont have same color
for i in range(0,4):
    if firstColors[i] == 'blue':
        secondColors[i] = 'red'
        colorIndexs[i+4] = 1
    else:
        secondColors[i] = 'blue'
        colorIndexs[i] = 1
colors = [firstColors, secondColors]


for n in range(0,2):
    # picks random trial and finds coordinates for each center
    randInt      = random.randint(0,300)
    shapeOne       = genCoor[randInt,0,:]
    shapeOne[0]   += n
    shapeTwo       = genCoor[randInt,1,:]
    shapeTwo[0]   += n
    shapeThree     = genCoor[randInt,2,:]
    shapeThree[0] += n
    shapeFour      = genCoor[randInt,3,:]
    shapeFour[0]  += n
    shapes = [shapeOne, shapeTwo, shapeThree, shapeFour]
    
    
    if rectangles:
        # creates rectangles at each center location
        rectVert = rectangleCreation(n,4)
        # creates numRect rectangles
        for k in range(0, numRect):
            stimRect[n][k] = ShapeStim(win, vertices = shapeVert[k][n], fillColor = colors[n][k], size = .5)
    else:
        # k cubes x 3 sides x 4 vertices
        cubeOne = cubeOneCreation(numCube)
        cubeTwo = cubeTwoCreation(numCube)
        for k in range(0,3):
            stimOneCube[n][k] = ShapeStim(win, vertices = cubeOne[n][k], fillColor = colors[n][0], size = .5)
            stimTwoCube[n][k] = ShapeStim(win, vertices = cubeTwo[n][k], fillColor = colors[n][1], size = .5)

fixation   = visual.Line(win, start = (-.025,0), end = (.025,0), lineColor = 'black', lineWidth = 4)
fixation2  = visual.Line(win, start = (0,-.025), end = (0,0.025), lineColor = 'black', lineWidth = 4)
arrowLeft = ShapeStim(win, vertices = [(.03,.04), (-.03,.04), (-.03,.05),(-.05,.04),(-.03,.03),(-.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)
arrowRight  = ShapeStim(win, vertices = [(-.03,.04), (.03,.04), (.03,.05),(.05,.04),(.03,.03),(.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)





















if rectangles:
    #while not event.getKeys():
    start = clock.getTime()
    stop  = 3
    while clock.getTime() - start < stop:
        fixation.draw()
        fixation2.draw()
        #arrowRight.draw()
        arrowLeft.draw()
        
        for k in range(0,numRect):
            stimRect[0][k].draw()
            stimRect[1][k].draw()
        win.flip()

    while clock.getTime() - start < 2*stop:
        fixation.draw()
        fixation2.draw()
        win.flip()

    number = random.randint(0,7)
    if number > 3:
        while clock.getTime() - start < 3*stop:
            fixation.draw()
            fixation2.draw()
            for k in range(numRect):
                stimRect[0][k].draw()
                stimRect[1][k].draw()
            win.flip()
else:
    #while not event.getKeys():
    start = clock.getTime()
    stop  = .4
    while clock.getTime() - start < stop:
        fixation.draw()
        fixation2.draw()
        for k in range(numCube):
            for j in range(3):
                stimOneCube[0][j].draw()
                stimOneCube[1][j].draw()
                stimTwoCube[0][j].draw()
                stimTwoCube[1][j].draw()
            
        win.flip()

    while clock.getTime() - start < stop + 1:
        fixation.draw()
        fixation2.draw()
        win.flip()
        
    if random.randint(0,7) > 3:
        while clock.getTime() - start < stop + 1.4:
            fixation.draw()
            fixation2.draw()
            for k in range(numCube):
                for j in range(3):
                    stimOneCube[0][j].draw()
                    stimOneCube[1][j].draw()
                    stimTwoCube[0][j].draw()
                    stimTwoCube[1][j].draw()
            win.flip()
    #else:
        #    while clock.getTime() - start < 3*stop:

win.close()
core.quit()