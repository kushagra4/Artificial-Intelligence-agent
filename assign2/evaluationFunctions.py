from scipy.spatial import distance
from watchYourBack import Board
from watchYourBack import Game


################################################################################
class Evaluation:
    #evaluation functon for the placing phase
    def evalFinal(state,colour, oppo_colour, evalWeights):
        #Board.printBoard(state)
        evaluation=0
        #print("________________________________________")
        if (evalWeights[0]!=0):
            evaluation+=evalWeights[0] * Evaluation.distanceLine(state, colour,
                                                                    oppo_colour)
        #print(evaluation)
        if (evalWeights[1]!=0):
            evaluation+=evalWeights[1] *Evaluation.PeiceAdvantage(state,colour,
                                                                    oppo_colour)
        #print(evaluation)
        if (evalWeights[2]!=0):
            evaluation+=evalWeights[2] *Evaluation.deathTrap(state,colour,
                                                                    oppo_colour)
        #print(evaluation)
        if (evalWeights[3]!=0):
            evaluation+=evalWeights[3]*Evaluation.evalFromCentre(state,colour,
                                                                    oppo_colour)
        #print(evaluation)
        if (evalWeights[4]!=0):
            evaluation+=evalWeights[4] *Evaluation.evalPartnerWarriorDiag(state,
                                                            colour,oppo_colour)
        #print(evaluation)
        if (evalWeights[5]!=0):
            evaluation+=evalWeights[5] *Evaluation.mainFourSquares(state,colour,
                                                                    oppo_colour)
        #print(evaluation)
        #print("________________________________________")
        return evaluation



####################################################################
    #This function returns the number of diagonal partners
    def EvalDiag(board, col,row, colour):
        return(Evaluation.checkDiagLeftUp(board,col,row, colour) +
        Evaluation.checkDiagLeftDown(board,col,row, colour) +
        Evaluation.checkDiagRightUp(board,col,row, colour) +
        Evaluation.checkDiagRightDown(board,col,row, colour))


    #returns 1 everytime there is partner which is diagonal
    def checkDiagLeftUp(board,col,row, colour):
        if (Board.validSquare(board,col-1,row-1) and (Board.comaprePieceat(
                                                board,col-1,row-1, colour))):
            return 1
        return 0
    def checkDiagLeftDown(board,col,row, colour):
        if (Board.validSquare(board,col-1,row+1) and (Board.comaprePieceat(
                                                    board,col-1,row+1, colour))):
            return 1
        return 0
    def checkDiagRightUp(board,col,row, colour):
        if (Board.validSquare(board,col+1,row-1) and (Board.comaprePieceat(
                                                    board,col+1,row-1, colour))):
            return 1
        return 0
    def checkDiagRightDown(board,col,row, colour):
        if (Board.validSquare(board,col+1,row+1) and (Board.comaprePieceat(
                                                    board,col+1,row+1, colour))):
            return 1
        return 0



    #returns normalised evaluation if there are peices diagonal
    def evalPartnerWarriorDiag(state,colour,oppo_colour):
        evaluation=0
        numberOfPeices=1
        for col in range(state.getMinColSize(),state.getMaxColSize()+1):
            for row in range(state.getMinRowSize(),state.getMaxRowSize()+1):
                if(Board.comaprePieceat(state,col,row,colour)):
                    numberOfPeices+=4
                    evaluation+=Evaluation.EvalDiag(state, col, row, colour)
                if(Board.comaprePieceat(state,col,row,oppo_colour)):
                    numberOfPeices+=4
                    evaluation-=Evaluation.EvalDiag(state, col, row, oppo_colour)



        return (evaluation/numberOfPeices)

####################################################################


    #returns the difference of the number of our player from the number of the
    #opponents players
    def PeiceAdvantage(state, colour, oppo_colour):
        eval=0
        for col in range (state.getMinColSize(),state.getMaxColSize()+1):
            for row in range (state.getMinRowSize(),state.getMaxRowSize()+1):
                if (Board.comaprePieceat(state,col,row, colour)):
                    eval+=1
                if (Board.comaprePieceat(state,col,row, oppo_colour)):
                    eval-=1
        return(eval)


####################################################################

#evaluation depending on the distnace form the line, if the player is white then
# from the line (0,2) otherwise if the
#player is black then from the line (0,6)

#only for placing phase
    def distanceLine(state, colour, oppo_colour):
        numberOfPeices=1
        eval=0
        if(colour=="W"):
            for col in range(state.getMinColSize(),state.getMaxColSize()+1):
                for row in range(state.getMinRowSize(),state.getMaxRowSize()+1):
                    if (Board.comaprePieceat(state,col,row, colour)):
                        numberOfPeices+=1
                        if(row>1):
                            eval+=(1/(row-1))
                        else:
                            eval+=0.75
                    if (Board.comaprePieceat(state,col,row, oppo_colour)):
                        numberOfPeices+=1
                        if(row<6):
                            eval-=(1/(6-row))
                        else:
                            eval-=0.75

        if(colour=="B"):
            for col in range(state.getMinColSize(),state.getMaxColSize()+1):
                for row in range(state.getMinRowSize(),state.getMaxRowSize()+1):
                    if (Board.comaprePieceat(state,col,row, colour)):
                        numberOfPeices+=1
                        if(row<6):
                            eval+=(1/(6-row))
                        else:
                            eval+=0.75
                    if (Board.comaprePieceat(state,col,row, oppo_colour)):
                        numberOfPeices+=1
                        if(row>1):
                            eval-=(1/(row-1))
                        else:
                            eval-=0.75

        return (eval/numberOfPeices)



################################################################################
    #returns the addition of distances from the center
    #inverses so closer is better
    def evalFromCentre(state,colour,oppo_colour):
        evaluation=0
        totPeices=1
        for col in range(state.getMinColSize(),state.getMaxColSize()+1):
            for row in range(state.getMinRowSize(),state.getMaxRowSize()+1):
                if(Board.comaprePieceat(state,col,row,colour)):
                    totPeices+=1
                    evaluation-=abs(distance.euclidean((col,row),(3.5,3.5)))
                if(Board.comaprePieceat(state,col,row,oppo_colour)):
                    totPeices+=1
                    evaluation+=abs(distance.euclidean((col,row),(3.5,3.5)))

        return (evaluation/(totPeices*(state.getMaxColSize()-2)))
    ################################################################################

    #number of death traps we have - number of death traps they have
    #death traps: squares which can be used to killanothe player
    def deathTrap(state,colour,oppo_colour):
        evaluation=0
        count=1
        for col in range(state.getMinColSize(),state.getMaxColSize()+1):
            for row in range(state.getMinRowSize(),state.getMaxRowSize()+1):
                if(Board.comaprePieceat(state,col,row,"E")):
                    count+=1
                    evaluation+=Evaluation.evalDeathTrap(state, col,row, colour)
                    evaluation-=Evaluation.evalDeathTrap(state, col,row,
                                                                    oppo_colour)
        return (evaluation/count)

    #this function adds to the evaluation values if we have two of the pieces of
    # the player separated by a square
    def evalDeathTrap(board, col, row, colour):
        eval=0
        if((Game.checkUpKill(board,col,row, colour)) and Game.checkDownKill(
                                                        board,col,row, colour)):
            eval+=1
        if((Game.checkRightKill(board,col,row, colour) and Game.checkLeftKill(
                                                    board,col,row, colour))):
            eval+=1
        return(eval)
################################################################################

    #this function adds to the evalution if our players are placed in the center
    # of the board otherwise subtracts from
    # the evaluation if the opponents players have occupied the center squares
    def mainFourSquares(state,colour, oppo_colour):
        eval=0
        if(Board.comaprePieceat(state,3,3,colour)):
            eval+=1
        if(Board.comaprePieceat(state,3,4,colour)):
            eval+=1
        if(Board.comaprePieceat(state,4,3,colour)):
            eval+=1
        if(Board.comaprePieceat(state,4,4,colour)):
            eval+=1
        if(Board.comaprePieceat(state,3,3,oppo_colour)):
            eval-=1
        if(Board.comaprePieceat(state,3,4,oppo_colour)):
            eval-=1
        if(Board.comaprePieceat(state,4,3,oppo_colour)):
            eval-=1
        if(Board.comaprePieceat(state,4,4,oppo_colour)):
            eval-=1
        return(eval/4)





######################################################
