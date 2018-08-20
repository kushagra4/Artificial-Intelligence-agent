import types
from watchYourBack import Board
from watchYourBack import Game
from evaluationFunctions import Evaluation
import minimax
################################################################################
#class which implements strategy pattern
class StrategyHub:
    def __init__(self, func= None):
        #use the function sent as the startegy
        if(func is not None):
            self.execute = types.MethodType(func,self)
    #excecute the startegy
    def execute(self, Board, colour,oppo_colour, type, no_turns):
        return(some)
################################################################################
#attacking strategy
def attackStrategy(self, Board, colour,oppo_colour, type, no_turns):
    FIRST_SHRINK=128
    SECOND_SHRINK=192
    #weights for the evaluation function and depth
    evalWeights=[1,3,0,2,0,2]
    depth=3

    #set distance line evaluating function to zero since its after placing phase
    if (type=="MP"):
        evalWeights[0]=0
    #switch this evaluation if its in this number of ranges: done to keep
    #time constraint
    if(no_turns>100 or no_turns<20 ):
        evalWeights[2]=2

    #Increase weights for eval from center when board get close to shrinking
    if(no_turns<=FIRST_SHRINK and no_turns>=96):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-96)
    if(no_turns<=SECOND_SHRINK and no_turns>=152):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-152)

    #increase depth when we shrink for the last time
    if(no_turns>SECOND_SHRINK):
        depth=4

    return(minimax.minimax(Board, colour,oppo_colour, type, evalWeights, depth))

################################################################################
#defending strategy
def defendStrategy(self, Board, colour,oppo_colour, type, no_turns):
    FIRST_SHRINK=128
    SECOND_SHRINK=192

    #weights for the evaluation function and depth
    evalWeights=[3,2,0,1,1,3]
    depth=3

    #set distance line evaluating function to zero since its after placing phase
    if (type=="MP"):
        evalWeights[0]=0

    #Increase weights for eval from center when board get close to shrinking
    if(no_turns<=FIRST_SHRINK and no_turns>=96):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-96)
    if(no_turns<=SECOND_SHRINK and no_turns>=152):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-152)

    #increase depth when we shrink for the last time
    if(no_turns>SECOND_SHRINK):
        depth=4
    #switch this evaluation if its in this number of ranges: done to keep
    #time constraint
    if(no_turns>100 or no_turns<20 ):
        evalWeights[2]=2



    return(minimax.minimax(Board, colour,oppo_colour, type, evalWeights, depth))
################################################################################
#godMode strategy
def godMode(self, Board, colour,oppo_colour, type, no_turns):
    FIRST_SHRINK=128
    SECOND_SHRINK=192
    #weights for the evaluation function and depth
    evalWeights=[3,2,0,2,0,5]
    depth=3


    #moving peices closer to the center when shrinking
    if(no_turns<=FIRST_SHRINK and no_turns>=96):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-96)
    if(no_turns<=SECOND_SHRINK and no_turns>=152):
        evalWeights[3]=evalWeights[3]+(0.6)*(no_turns-152)


    #set distance line evaluating function to zero since its after placing phase
    if (type=="MP"):
        evalWeights[0]=0
    


    #increase depth when we shrink for the last time
    if(no_turns>SECOND_SHRINK):
        depth=4

    return(minimax.minimax(Board, colour,oppo_colour, type, evalWeights, depth))
################################################################################
#massacre strategy
def massacre(self, Board, colour,oppo_colour, type, no_turns):
    SECOND_SHRINK=192
    #weights for the evaluation function and depth
    evalWeights=[0,2,0,1,0,1]
    depth=3


    #increase depth when we shrink for the last time
    if(no_turns>SECOND_SHRINK):
        depth=4

    return(minimax.minimax(Board, colour,oppo_colour, type, evalWeights, depth))
