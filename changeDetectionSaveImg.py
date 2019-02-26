### Micah Ketola 
### Summer 2018
### CSNE Summer Program
### Change Detection Paradigm with different stimuli

from __future__ import absolute_import, division, print_function
from builtins import str
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.iohub import launchHubServer
from psychopy.visual import ShapeStim 
import random
import math
import pickle
import time
import numpy
import pylab
import os  # handy system and path functions
import sys  # to get file system encoding

def main(fCue,fStim,fInterval,fTest,fPause,recLength,recWidth,cubeLength,cubeWidth,tPerBlock,stimType,targChange,trialType,cue,numTrials):
    
    fCue = fCue
    fStim = fStim
    fTest = fTest
    fPause = fPause
    recLength = recLength
    recWidth = recWidth
    cubeLength = cubeLength
    cubeWidth = cubeWidth
    tPerBlock = tPerBlock
    stimType = stimType 
    targChange = targChange
    trialType = trialType
    cue = cue
    numTrials = numTrials 
    
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
    os.chdir(_thisDir + u'\%s%s%s' %(stimType,trialType[0],cue[0]))

    # Store info about the experiment session
    expName = 'Change Detection.py'
    expInfo = {'session': '001', 'participant': ''}
    dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])

    # An ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=filename)
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    
    # 300 x 4 x 2 matrix 
    # 300 entries, 4 shapes, xy for each shape
    f = open('genCoor.pckl', 'rb')
    genCoor = pickle.load(f)
    f.close()
    win = visual.Window([1600, 900], units = 'height', fullscr=True)
    clock = core.Clock()

    # KEYBOARD STUFF
    # Start iohub process. The iohub process can be accessed using `io`.
    io = launchHubServer()
    # A `keyboard` variable is used to access the iohub Keyboard device.
    keyboard = io.devices.keyboard
    events = keyboard.getKeys()
    
    # INITIALIZE
    # trialN       : number of trial
    # trialResp    : their response on each trial
    # correctResp  : if their response was correct
    # responseTime : the amount of time it took for them to respond on each trial
    m = 0
    trialN       = [-1 for x in range(numTrials)]
    trialResp    = [9 for x in range(numTrials)]
    correctResp  = [9 for x in range(numTrials)]
    responseTime = [0 for x in range(numTrials)]
    respChar     = [['r','i'],['f','j']]
    numStim      = [[2,4,4],[1,2,2]]
    
    # Which stim to display
    # true if rectangles, false if cubes
    rectangles = not stimType
    nStim      = numStim[stimType][trialType[0]]
    shapeN     = [[],[]]
    recStim    = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
    recVert    = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
    cubeVert   = []
    cubeV      = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
    cubeStim   = [[[[],[],[]] for i in range(nStim)],[[[],[],[]] for i in range(nStim)]]

    # COLORS
    recColors  = [[['blue','blue'],['blue','blue']],[['red','red','blue','blue'],['red','red','blue','blue']],[['blue','blue','blue','blue'],['blue','blue','blue','blue']]]
    blues      = ['#0000ff','#9999ff','#000066']
    reds       = ['#ff0000' ,'#ff9999','#660000']
    randBlue   = random.sample(blues,3)
    randRed    = random.sample(reds,3)
    cubeColors = [[[randBlue],[randBlue]],[[randRed,randBlue],[randRed,randBlue]],[[randBlue,randBlue],[randBlue,randBlue]]]
    
    # STIMULI
    center     = [0,0]
    posTheta   = [[0, math.pi/4, math.pi/2, 3*math.pi/4],[0, math.pi/4, math.pi/2, 3*math.pi/4]]
    posCubes   = [0, 1, 0, 1]
    pauseText  = visual.TextStim(win, text = "Press the Spacebar to Continue", font=u'Arial', pos=(0, 0), height=0.1, wrapWidth=None, ori=0, color=u'white', colorSpace='rgb', opacity=1, depth=0.0)
    fixation   = visual.Line(win, start = (-.025,0), end = (.025,0), lineColor = 'black', lineWidth = 4)
    fixation2  = visual.Line(win, start = (0,-.025), end = (0,0.025), lineColor = 'black', lineWidth = 4)
    arrowLeft  = ShapeStim(win, vertices = [(.03,.04), (-.03,.04), (-.03,.05),(-.05,.04),(-.03,.03),(-.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)
    arrowRight = ShapeStim(win, vertices = [(-.03,.04), (.03,.04), (.03,.05),(.05,.04),(.03,.03),(.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)

    # rotates [x,y] by theta
    def rotate(xy,center,theta):
        #pts = {} Rotates points(nx2) about center by angle theta in radians
        return numpy.dot(xy-center,numpy.array([[math.cos(theta),math.sin(theta)],[-math.sin(theta),math.cos(theta)]]))+center
        
    def rotateRec(center,theta):
        center = center
        theta = theta
        p1 = [center[0]-recWidth, center[1]-recLength]
        p2 = [center[0]-recWidth, center[1]+recLength]
        p3 = [center[0]+recWidth, center[1]+recLength]
        p4 = [center[0]+recWidth, center[1]-recLength]
        rVert = rotate(numpy.array([p1, p2, p3, p4]),center,theta)
        return rVert

    # creates a three-sided cube
    def cubeCreator(centerV, cubeType):
        center = centerV
        cubeType = cubeType
        if cubeType == 0:
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
        else:
            m1 = [center[0]          , center[1]]
            m2 = [center[0]          , center[1]+cubeLength]
            m3 = [center[0]+cubeWidth, center[1]+cubeLength/2]
            m4 = [center[0]+cubeWidth, center[1]-cubeLength/2]
            sideOne = [m1, m2, m3, m4]
            
            n1 = [center[0]          , center[1]]
            n2 = [center[0]          , center[1]+cubeLength]
            n3 = [center[0]-cubeWidth, center[1]+cubeLength/2]
            n4 = [center[0]-cubeWidth, center[1]-cubeLength/2]
            sideTwo = [n1, n2, n3, n4]
            
            s1 = [center[0]          , center[1]]
            s2 = [center[0]-cubeWidth, center[1]-cubeLength/2]
            s3 = [center[0]          , center[1]-cubeLength]
            s4 = [center[0]+cubeWidth, center[1]-cubeLength/2]
            sideThree = [s1, s2, s3, s4]
            # k cubes x 3 sides x 4 vertices x 2 coordinates
        cVert = [sideOne, sideTwo, sideThree]
        return cVert
        

    def randShuf(inputList):
        shufList = inputList[:]
        while True:
            random.shuffle(shufList)
            for a, b in zip(inputList, shufList):
                if a == b:
                    break
                else:
                    return shufList
                    
    def recDraw(frames, nStim, stimulus,changeT):
                frames = frames
                fixation.draw()
                fixation2.draw()
                for k in range(nStim):
                    stimulus[0][k].draw()
                    stimulus[1][k].draw()
                print('stimType%d_trialType%d_cue%d_%d_order%d.png' % (stimType,trialType[0], cue[0],t,changeT))
                time.sleep(0.03)
                win.getMovieFrame(buffer = 'back')
                win.flip()
                win.saveMovieFrames('stimType%d_trialType%d_cue%d_%d_order%d.png' % (stimType,trialType[0], cue[0],t,changeT))

    def cubeDraw(frames, nStim, stimulus,changeT):
                frames = frames
                fixation.draw()
                fixation2.draw()
                for j in range(nStim):
                    for k in range(3):
                        stimulus[0][j][k].draw()
                        stimulus[1][j][k].draw()
                print('stimType%d_trialType%d_cue%d_%d_order%d.png' % (stimType,trialType[0], cue[0],t,changeT))
                time.sleep(0.03)
                win.getMovieFrame(buffer = 'back')
                win.flip()
                win.saveMovieFrames('stimType%d_trialType%d_cue%d_%d_order%d.png' % (stimType,trialType[0], cue[0],t,changeT))

    for t in range(numTrials):
        print(t)
        if (t % tPerBlock == 0) & (t > 1):
            waiting = []
            while not ' ' in waiting:
                pauseText.draw()
                win.flip()
                waiting = keyboard.getKeys()
        random.shuffle(recColors[0][0])
        trialN[t] = t + 1
        nStim = numStim[stimType][trialType[t]]
        recStim  = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
        recVert  = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
        cubeV    = [[[] for i in range(nStim)],[[] for i in range(nStim)]]
        cubeStim = [[[[],[],[]] for i in range(nStim)],[[[],[],[]] for i in range(nStim)]]
        
        for n in range(2):
            # picks random trial and finds coordinates for four centers
            randInt = random.randint(0,299)
            shapeOne       = genCoor[randInt,0,:]
            shapeOne[0]   += (n * 1.8)
            shapeTwo       = genCoor[randInt,1,:]
            shapeTwo[0]   += (n * 1.8)
            shapeThree     = genCoor[randInt,2,:]
            shapeThree[0] += (n * 1.8)
            shapeFour      = genCoor[randInt,3,:]
            shapeFour[0]  += (n * 1.8)
            shapes = [shapeOne, shapeTwo, shapeThree, shapeFour]
            shapeN[n] = shapes
            
            if rectangles:
                random.shuffle(posTheta[n])
                # creates numRect rectangles with random orientations
                for k in range(nStim):
                    recVert[n][k] = rotateRec(shapes[k],posTheta[n][k])
                    recStim[n][k] = ShapeStim(win, vertices = recVert[n][k], fillColor = recColors[trialType[t]][n][k], size = .5)
            else:
                random.shuffle(posCubes)
                for j in range(nStim):
                    # numCube x 3 sides x 4 vertices
                    cubeVert = cubeCreator(shapes[j],posCubes[j])
                    cubeV[n][j] = cubeCreator(shapes[j],posCubes[j])
                    for i in range(3):
                        # numCube x 3 sides
                        cubeStim[n][j][i] = ShapeStim(win,vertices = cubeVert[i], fillColor = cubeColors[trialType[t]][n][j][i], size = .5)



        # STIM PRESENTATION
        
        # presents cue
        #for frameN in range(fCue + 1):
        #    fixation.draw()
        #    fixation2.draw()
        #   if cue[t]:
        #       arrowRight.draw()
        #    else:
        #        arrowLeft.draw()
        #    win.flip()
        
        # presents stim
        if rectangles:
            recDraw(fStim, nStim, recStim,0)
        else:
            cubeDraw(fStim, nStim, cubeStim,0)
        
        # presents interval
        #for frameN in range(fInterval + 1):
        #    fixation.draw()
        #    fixation2.draw()
        #    win.flip()

        # presents test array
        if rectangles:
            if targChange[t]:
                stimChange = random.randint(0,nStim-1)
                stimC = recColors[trialType[t]][cue[t]][stimChange]
                while stimC != 'blue':
                    stimChange = random.randint(0,nStim-1)
                    stimC = recColors[trialType[t]][cue[t]][stimChange]
                #change the orientation of the rectangle chosen
                if posTheta[cue[t]][stimChange] == math.pi/2:
                    angleChange = 0
                else:
                    angleChange = math.pi/2
                recStim[cue[t]][stimChange] = ShapeStim(win, vertices = rotateRec(shapeN[cue[t]][stimChange],angleChange), fillColor = recColors[trialType[t]][cue[t]][stimChange], size = .5)
                recDraw(fTest, nStim, recStim,1)
            else:
                recDraw(fTest, nStim, recStim,0)
        else:
            if targChange[t]:
                stimChange = random.randint(0,nStim-1)
                while not '#0000ff' in cubeColors[trialType[t]][cue[t]][stimChange]:
                    stimChange = random.randint(0,nStim-1)
                #change the shading of the rectangle chosen
                newColors = randShuf(cubeColors[trialType[t]][cue[t]][stimChange])
                print("got here")
                for i in range(3):
                    # numCube x 3 sides
                    cubeStim[cue[t]][stimChange][i] = ShapeStim(win, vertices = cubeV[cue[t]][stimChange][i], fillColor = newColors[i], size = .5)
                cubeDraw(fTest, nStim, cubeStim,1)
            else:
                cubeDraw(fTest, nStim, cubeStim,0)
            
        # presents interval
        for frameN in range(fPause + 1):
            fixation.draw()
            fixation2.draw()
            win.flip()
        
        if trialResp[t] == targChange[t]:
            correctResp[t] = 1
        else:
            correctResp[t] = 0

    # OUTPUT
    print()
    print('Correct response trials')
    print(correctResp)
    print('Percent correct')
    print(sum(correctResp) / numTrials)
    print('Response Time')
    print(responseTime)
    print('Average response time')
    print(sum(responseTime) / numTrials)
    
    
    thisExp.addData('correct responses',correctResp)
    thisExp.nextEntry()
    thisExp.addData('response times', responseTime)
    thisExp.nextEntry()
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    
    origLUT = numpy.round(win.backend._origGammaRamp * 65535.0).astype("uint16")
    origLUT = origLUT.byteswap() / 255.0
    win.backend._origGammaRamp = origLUT
    
    win.close()
    core.quit()