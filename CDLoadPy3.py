### Micah Ketola 
### Summer 2018
### CSNE Summer Program
### Change Detection Paradigm with different stimuli

from __future__ import absolute_import, division, print_function
from builtins import str
from psychopy import data, logging, visual, sound, core, event, clock
from psychopy.iohub.client import launchHubServer
from psychopy.visual import ShapeStim 
import time
import random
import math
import pickle
import numpy
import pylab
import os  # handy system and path functions
import sys  # to get file system encoding

def main(fCue,fStim,fInterval,fTest,fPause,tPerBlock,stimType,targChange,trialType,cue,numTrials,blocks):
    
    fCue = fCue
    fStim = fStim
    fTest = fTest
    fPause = fPause
    tPerBlock = tPerBlock
    stimType = stimType 
    targChange = targChange
    trialType = trialType
    cue = cue
    numTrials = numTrials 
    
    _thisDir = "C:/Users/Mark Pettet/Documents/MK/"
    
    # Store info about the experiment session
    expName = 'Change Detection.py'
    expInfo = {'session': '001', 'participant': ''}
    expInfo['date'] = data.getDateStr()  # add a simple timestamp
    expInfo['expName'] = expName

    # Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    exp = data.ExperimentHandler(name=expName,
                    version='0.1',
                    extraInfo={'participant':'jwp', 'ori':45},
                    runtimeInfo=None,
                    originPath=None,
                    savePickle=True,
                    saveWideText=True,
                    dataFileName=filename)
    
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    
    win = visual.Window(size = [1600, 900], units = 'height', fullscr=True)
    
    print("keyboard")
    # KEYBOARD STUFF
    # Start iohub process. The iohub process can be accessed using `io`.
    io = launchHubServer()
    # A `keyboard` variable is used to access the iohub Keyboard device.
    keyboard = psychopy.iohub.client.keyboard.Keyboard
    events = keyboard.getKeys()
    print("exp start")
    
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
    pauseTime    = [0 for x in range(blocks)]
    respChar     = [['r','i'],['f','j']]
    
    # Which stim to display
    # true if rectangles, false if cubes
    rectangles = not stimType
    
    # STIMULI
    pauseText  = visual.TextStim(win, text = "Press the Spacebar to Continue", font=u'Arial', pos=(0, 0), height=0.1, wrapWidth=None, ori=0, color=u'white', colorSpace='rgb', opacity=1, depth=0.0)
    fixation   = visual.Line(win, start = (-.025,0), end = (.025,0), lineColor = 'black', lineWidth = 4)
    fixation2  = visual.Line(win, start = (0,-.025), end = (0,0.025), lineColor = 'black', lineWidth = 4)
    arrowLeft  = ShapeStim(win, vertices = [(.03,.04), (-.03,.04), (-.03,.05),(-.05,.04),(-.03,.03),(-.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)
    arrowRight = ShapeStim(win, vertices = [(-.03,.04), (.03,.04), (.03,.05),(.05,.04),(.03,.03),(.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)

    
    for t in range(numTrials):
        print(t)
        trialTime = time.time()
        if (t % tPerBlock == 0) & (t > 1):
            event.clearEvents(eventType='keyboard')
            waiting = []
            tStart = time.time()
            while not 'space' in waiting:
                waiting = event.getKeys(keyList=['space'])
                pauseText.draw()
                win.flip()
            pauseTime = time.time() - tStart
            thisExp.addData('pauseTime', pauseTime)
        
        trialN[t] = t + 1
        
        # STIM PRESENTATION
        randTrial = random.randint(1,100)
        stimName  = 'stimType%d_trialType%d_cue%d_order%d (%d).png' % (stimType, trialType[t], cue[t], 0, randTrial)
        stimDir      = '%d%d%d/' % (stimType, trialType[t], cue[t]) + stimName
        
        print(t + .5)

        # presents cue
        for frameN in range(fCue + 1):
            fixation.draw()
            fixation2.draw()
            if cue[t]:
                arrowRight.draw()
            else:
                arrowLeft.draw()
            win.flip()
        
        # presents stim
        for frameN in range(fStim + 1):
            stim = visual.ImageStim(win, image = stimDir)
            stim.draw()
            win.flip()
            
        
        # presents interval
        for frameN in range(fInterval + 1):
            fixation.draw()
            fixation2.draw()
            win.flip()

        # presents test array
        if targChange[t]:
            stimName  = 'stimType%d_trialType%d_cue%d_order%d (%d).png' % (stimType, trialType[t], cue[t], 1, randTrial)
            stimDir   = '%d%d%d/' % (stimType, trialType[t], cue[t]) + stimName
            stim      = visual.ImageStim(win, image = stimDir)
            
        startT = time.time()
        for frameN in range(fTest + 1):
            theseKeys = event.getKeys(keyList=['r', 'f', 'i', 'j'])
            if len(theseKeys) > 0:  # at least one key was pressed
                trialResp[t]    = theseKeys[-1]  # just the last key pressed
                responseTime[t] = time.time() - startT
            stim.draw()
            win.flip()
            
        # presents interval
        for frameN in range(fPause + 1):
            fixation.draw()
            fixation2.draw()
            win.flip()
        
        if cue[t]:
            if targChange[t]:
                if trialResp[t] == 'i':
                    correctResp[t] = 1
                else:
                    correctResp[t] = 0
            else:
                if trialResp[t] == 'j':
                    correctResp[t] = 1
                else:
                    correctResp[t] = 0
        else:
            if targChange[t]:
                if trialResp[t] == 'r':
                    correctResp[t] = 1
                else:
                    correctResp[t] = 0
            else:
                if trialResp[t] == 'f':
                    correctResp[t] = 1
                else:
                    correctResp[t] = 0
                    
        # OUTPUT 
        thisExp.addData('stimType', stimType)
        thisExp.addData('trialType', trialType[t])
        thisExp.addData('targChange', targChange[t])
        thisExp.addData('cue', cue[t])
        thisExp.addData('startTime', trialTime)
        thisExp.addData('responseTime', responseTime[t])
        thisExp.addData('trialKeyPress', trialResp[t])
        thisExp.addData('correctResponse',correctResp[t])
        thisExp.addData('trialNumber', trialN[t])
        thisExp.addData('stimulusHandle', stimName)
        thisExp.nextEntry()
            
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()
    # make sure everything is closed down
    thisExp.abort()  # or data files will save again on exit
    io.quit()
    win.close()
    core.quit()