import random
import copy

TYPES = [0,1]
LOADS = [0,1,2]
SIDES  = [0,1]

TRIAL_TYPES = [(x, y, z) for x in TYPES for y in LOADS for z in SIDES]

def generate_trial():
    trials = []
    for j in range(5):
        trials += copy.copy(TRIAL_TYPES)
    random.shuffle(trials)
    return trials
    
def generate_block():
    blocks = []
    for j in range(2):
        blocks += generate_trial()
    random.shuffle(blocks)
    return blocks

def generate_experiment():
    exp = []
    for j in range(4):
        exp += generate_block()
    return exp

