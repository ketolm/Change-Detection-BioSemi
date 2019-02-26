# Client Change-Detection Script
from changeDetectionSaveImg import main
from trialGenerator import generate_trial, generate_block, generate_experiment
import pickle



# PARTICIPANT'S INITIALS
participant     = '001'

# WANT TO GET TO 8 AND 8
rectangleBlocks = 0
cubeBlocks      = 0





################################ 
# DON'T WORRY ABOUT THIS STUFF #
################################

# PARAMETERS
# targC     : 0 if no change,  1 if change
# stimType  : 0 if rectangles, 1 if cubes
# trialT    : 0 if 2,          1 if 4,     2 if 2+2
#             0 if 1,          1 if 1 + 1, 2 if 2
# cueT      : 0 if left,       1 if right
targC      = 1

stimType   = 0
trialT     = 1
cueT       = 0


blocks     = 1
tPerBlock  = 200


# TIMING
# each frame is 16.666667 ms
fCue       = 1  # 200 ms
fStim      = 1  # 100 ms
fInterval  = 1  # 900 ms
fTest      = 1  # 2000 ms 
fPause     = 1  # 1000 ms 

# STIM SIZE
recLength  = .09
recWidth   = .27
cubeLength = .25
cubeWidth  = .25

# TRIAL SEQUENCING

# targChange: 0 if no change, 1 if change
# trialType : 0 if min targets only, 1 if targets with distractors, 2 if max targets only
# cue       : 0 if left, 1 if right
numTrials  = blocks*tPerBlock
blocksDone = rectangleBlocks + cubeBlocks
cue        = []
trialType  = []
targChange = []
for j in range(300):
    targChange.append(targC)
    trialType.append(trialT)
    cue.append(cueT)
print(len(targChange))



block = main(fCue,fStim,fInterval,fTest,fPause,recLength,recWidth,cubeLength,cubeWidth,tPerBlock,stimType,targChange,trialType,cue,numTrials)




