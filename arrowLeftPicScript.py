from __future__ import absolute_import, division, print_function
from builtins import str
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.iohub import launchHubServer
from psychopy.visual import ShapeStim 
import random
import math
import pickle
import numpy
import pylab

win = visual.Window([1600, 900], units = 'height', fullscr=True)


fixation   = visual.Line(win, start = (-.025,0), end = (.025,0), lineColor = 'black', lineWidth = 4)
fixation2  = visual.Line(win, start = (0,-.025), end = (0,0.025), lineColor = 'black', lineWidth = 4)
arrowLeft  = ShapeStim(win, vertices = [(.03,.04), (-.03,.04), (-.03,.05),(-.05,.04),(-.03,.03),(-.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)
arrowRight = ShapeStim(win, vertices = [(-.03,.04), (.03,.04), (.03,.05),(.05,.04),(.03,.03),(.03,.04)], lineColor = 'black',fillColor = 'black', lineWidth = 3)

fixation.draw()
fixation2.draw()
arrowRight.draw()
win.getMovieFrame(buffer = 'back')
win.flip()
win.saveMovieFrames('arrowRight.png')