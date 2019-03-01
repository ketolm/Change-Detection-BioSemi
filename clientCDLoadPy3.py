# Client Change-Detection Script
from CDLoadPy3 import main
from trialGenerator import generate_trial, generate_block, generate_experiment
import pickle



# PARTICIPANT'S INITIALS
participant     = ''

# WANT TO GET TO 8 AND 8
rectangleBlocks = 0
cubeBlocks      = 0


# 4 cube, 4 rec, 4 cube, 4 rec







































################################ 
# DON'T WORRY ABOUT THIS STUFF #
################################
if rectangleBlocks == 0 & cubeBlocks == 0:
    trials = generate_experiment()
    with open(participant + 'ChangeDE','wb') as fp:
        pickle.dump(trials,fp)

with open(participant + 'ChangeDE','rb') as fp:
        trials = pickle.load(fp)


# PARAMETERS
# stimType  : 0 if rectangles, 1 if cubes
stimType   = 1
blocks     = 2
tPerBlock  = 2


# TIMING
# each frame is 16.666667 ms
fCue       = 12  # 12  200 ms
fStim      = 6   # 6   100 ms
fInterval  = 54  # 54  900 ms
fTest      = 120 # 120 2000 ms 
fPause     = 60  # 60  1000 ms 

# TRIAL SEQUENCING
# targChange: 0 if no change, 1 if change
# trialType : 0 if min targets only, 1 if targets with distractors, 2 if max targets only
# cue       : 0 if left, 1 if right
numTrials  = blocks*tPerBlock
blocksDone = rectangleBlocks + cubeBlocks
cue        = []
trialType  = []
targChange = []
for j in range(blocksDone * numTrials, numTrials + blocksDone * numTrials):
    targChange.append(trials[j][0])
    trialType.append(trials[j][1])
    cue.append(trials[j][2])

block = main(fCue,fStim,fInterval,fTest,fPause,tPerBlock,stimType,targChange,trialType,cue,numTrials,blocks)




