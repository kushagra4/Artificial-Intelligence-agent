
# coding: utf-8
import math
import copy
from scipy.spatial import distance
from watchYourBack import Board
from watchYourBack import Game


class Evaluation:




    #evaluation functon for the placing phase
    def eval1(state,colour, oppo_colour):
        evaluation=Evaluation.distanceLine(state, colour, oppo_colour) +  Evaluation.PeiceAdvantage(state,colour, oppo_colour) + Evaluation.deathTrap(state,colour,oppo_colour) - 4*Evaluation.evalFromCentre(state,colour,oppo_colour) + Evaluation.evalPartnerWarriorDiag(state,colour,oppo_colour)
        return evaluation
    #evaluation function for the moving phase
    def eval2(state,colour, oppo_colour):
        evaluation=Evaluation.distanceLine(state, colour, oppo_colour) + Evaluation.PeiceAdvantage(state,colour, oppo_colour) + Evaluation.deathTrap(state,colour,oppo_colour)- 4*Evaluation.evalFromCentre(state,colour,oppo_colour) + Evaluation.evalPartnerWarriorDiag(state,colour,oppo_colour)
        return evaluation



####################################################################
    def EvalDiag(board, col,row, colour):
        return(Evaluation.checkDiagLeftUp(board,col,row, colour) + Evaluation.checkDiagLeftDown(board,col,row, colour) + Evaluation.checkDiagRightUp(board,col,row, colour) + Evaluation.checkDiagRightDown(board,col,row, colour))



    def checkDiagLeftUp(board,col,row, colour):
        if (Board.validSquare(board,col-1,row-1) and (Board.comaprePieceat(board,col-1,row-1, colour))):
            return 1
        return 0
    def checkDiagLeftDown(board,col,row, colour):
        if (Board.validSquare(board,col-1,row+1) and (Board.comaprePieceat(board,col-1,row+1, colour))):
            return 1
        return 0
    def checkDiagRightUp(board,col,row, colour):
        if (Board.validSquare(board,col+1,row-1) and (Board.comaprePieceat(board,col+1,row-1, colour))):
            return 1
        return 0
    def checkDiagRightDown(board,col,row, colour):
        if (Board.validSquare(board,col+1,row+1) and (Board.comaprePieceat(board,col+1,row+1, colour))):
            return 1
        return 0
####################################################################

    #returns the number of peices left of that colour
    def piecesLeft(state, colour):
        count=0
        for col in range (0,8):
            for row in range (0,8):
                if (Board.comaprePieceat(state,col,row, colour)):
                    count+=1
        return count

    def PeiceAdvantage(state, colour, oppo_colour):
        eval=Evaluation.piecesLeft(state,colour)-Evaluation.piecesLeft(state,oppo_colour)
        return(eval/12)





####################################################################

#evaluation depending on the distnace form the ine
    def distanceLine(state, colour, oppo_colour):
        numberOfPeices=1
        eval=0
        if(colour=="W"):
            for col in range(0,8):
                for row in range(0,6):
                    if (Board.comaprePieceat(state,col,row, colour)):
                        numberOfPeices+=1
                        if(row>1):
                            eval+=(1/(row-1))
                        else:
                            eval+=0.75


        if(colour=="B"):
            for col in range(0,8):
                for row in range(2,8):
                    if (Board.comaprePieceat(state,col,row, colour)):
                        numberOfPeices+=1
                        if(row<6):
                            eval+=(1/(6-row))
                        else:
                            eval+=0.75
        return (eval/numberOfPeices)


    #return eval if there are peices diagonal
    def evalPartnerWarriorDiag(state,colour,oppo_colour):
        evaluation=0
        numberOfPeices=1
        if(colour=="W"):
            for col in range(0,8):
                for row in range(0,6):
                    if(Board.comaprePieceat(state,col,row,"W")):
                        numberOfPeices+=1
                        evaluation+=Evaluation.EvalDiag(state, col, row, colour)
        if(colour=="B"):
            for col in range(0,8):
                for row in range(2,8):
                    if(Board.comaprePieceat(state,col,row,"B")):
                        numberOfPeices+=1
                        evaluation+=Evaluation.EvalDiag(state,col, row, colour)


        return (evaluation/numberOfPeices)

    #returns the addition of distances from the center
    def evalFromCentre(state,colour,oppo_colour):
        evaluation=0
        totPeices=0
        if(colour=="W"):
            for col in range(0,8):
                for row in range(0,6):
                    if(Board.comaprePieceat(state,col,row,"W")):
                        totPeices+=1
                        evaluation+=distance.euclidean((col,row),(3.5,3.5))

        if(colour=="B"):
            for col in range(0,8):
                for row in range(2,8):
                    if(Board.comaprePieceat(state,col,row,"W")):
                        totPeices+=1
                        evaluation+=distance.euclidean((col,row),(3.5,3.5))


        return evaluation

    #number of death traps we have - number of death traps they have
    def deathTrap(state,colour,oppo_colour):
        evaluation=0
        for col in range(0,8):
            for row in range(0,8):
                if(Board.comaprePieceat(state,col,row,"E")):
                    evaluation+=Evaluation.evalDeathTrap(state, col,row, colour)
                    evaluation-=Evaluation.evalDeathTrap(state, col,row, oppo_colour)
        return evaluation

    def evalDeathTrap(board, col, row, colour):
        eval=0
        if((Game.checkUpKill(board,col,row, colour)) and Game.checkDownKill(board,col,row, colour)):
            eval+=1
        if((Game.checkRightKill(board,col,row, colour) and Game.checkLeftKill(board,col,row, colour))):
            eval+=1
        return(eval)






######################################################

class Player:
    board=Board()
    team_colour=None
    oppo_colour=None
    plasingPhase=True
    no_turns=0
    our_turns=-1


    def __init__(self,colour):
        if (colour=="white"):
            self.team_colour="W"
            self.oppo_colour="B"
        else:
            self.team_colour="B"
            self.oppo_colour="W"



########################################################


    # countMoves calculates all the possible moves a single piece can make and
    #sums it up
    def checkMove(board, col, row):
        possibleMoves = []

        # Check up if its free and in the board range
        if (Board.validSquare(board,col,row-1) and Board.comaprePieceat(board,col,row - 1, "E")):
            possibleMoves.append([col,row-1])

        # Check up for a jump over another piece
        elif (Board.validSquare(board,col,row-2) and not (Board.comaprePieceat(board,col,row - 1, "E")) and Board.comaprePieceat(board,col,row-2,"E")):
            possibleMoves.append([col,row-2])

        # Check down if its free and in the board range
        if (Board.validSquare(board,col,row+1) and Board.comaprePieceat(board,col,row + 1, "E")):
            possibleMoves.append([col,row+1])
        # Check down for a jump over another piece
        elif (((Board.validSquare(board,col,row+2)) and not(Board.comaprePieceat(board,col,row - 1, "E"))) and (Board.comaprePieceat(board,col,row + 2, "E"))):
            possibleMoves.append([col,row+2])

              # check left if its free and in the board range
        if (Board.validSquare(board,col-1,row) and Board.comaprePieceat(board,col-1, row, "E")):
            possibleMoves.append([col-1,row])
        # check left for a jump over another piece
        elif ((Board.validSquare(board,col-2,row) and not(Board.comaprePieceat(board,col-1,row, "E"))) and
                    (Board.comaprePieceat(board,col-2,row, "E"))):
            possibleMoves.append([col-2,row])

        # check right if its free and in the board range
        if (Board.validSquare(board,col+1,row) and (Board.comaprePieceat(board,col+1,row, "E"))):
            possibleMoves.append([col+1,row])
        # check right for a jump over another piece
        elif ((Board.validSquare(board,col+2,row) and not(Board.comaprePieceat(board,col+1,row, "E")))
              and (Board.comaprePieceat(board,col+2,row, "E"))):
            possibleMoves.append([col+2,row])
        #return the total number of moves available for that piece
        return possibleMoves


    # countTotalMoves iterates through the board and sums up the total number
    #of possible moves for each of the players
    def countTotalMoves(board,colour):
        moves = 0
        for row in range(Board.getMinRowSize(board), Board.getMaxRowSize(board)+1):
            for col in range(Board.getMinColSize(board), Board.getMaxColSize(board)+1):
                if not(Board.comaprePieceat(board,col,row, "E")):
                    if not(Board.comaprePieceat(board,col,row, colour)):
                        moves += Player.countMoves(board,row, col)

        return moves



########################################################



########################################################
    #total counts in a placing phase
    def placingPhaseMoves(board,colour):
        moves=0

        if(colour == "W"):
            for col in range (0,8):
                for row in range (0,6):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        moves+=1

        if(colour == "B"):
            for col in range (0,8):
                for row in range (2,8):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        moves+=1
        return moves






########################################################


    #gets a successors of the board
    def getSuccessors(board, colour, output, type):


        Successors=[]
        #if its in the placing phase then get states for that phase
        if (type=="PP"):

            #if you want the board as the output
            if (output=="boards"):
                if(colour == "W"):
                    for col in range (0,8):
                        for row in range (0,6):
                            if (Board.comaprePieceat(board,col,row, "E")):
                                tempBoard=copy.deepcopy(board) #make a copy of the board that will represent a new state
                                Board.placePiece(tempBoard,col,row,"W")
                                Game.removeKills(tempBoard) # check if after placing the piece there is something
                                # that can be eliminated from the board and remove it from the board
                                Successors.append(tempBoard)

                if(colour == "B"):
                    for col in range (0,8):
                        for row in range (2,8):
                            if (Board.comaprePieceat(board,col,row, "E")):
                                tempBoard=copy.deepcopy(board) #make a copy of the board that will represent a new state
                                Board.placePiece(tempBoard,col,row,"B")
                                Game.removeKills(tempBoard) # check if after placing the piece there is something
                                # that can be eliminated from the board and remove it from the board
                                Successors.append(tempBoard)
            #if you want the output as coordinates
            else:
                if(colour == "W"):
                    for col in range (0,8):
                        for row in range (0,6):
                            if (Board.comaprePieceat(board,col,row, "E")):
                                Successors.append((col,row))

                if(colour == "B"):
                    for col in range (0,8):
                        for row in range (2,8):
                            if (Board.comaprePieceat(board,col,row, "E")):
                                Successors.append((col,row))

        # if its in the moving phase then get states for that phase
        if (type=="MP"):
            if (output=="boards"):
                for row in range(Board.getMinRowSize(board), Board.getMaxRowSize(board)+1):
                    for col in range(Board.getMinColSize(board), Board.getMaxColSize(board)+1):
                        if (Board.comaprePieceat(board,col,row, colour )):
                            temp=Player.checkMove(board,col, row)
                            for pos in temp:
                                tempBoard=copy.deepcopy(board) #make a copy of the board that will represent a new state
                                Board.movePiece(tempBoard,col,row,pos[0],pos[1])
                                Game.removeKills(tempBoard)
                                Successors.append(tempBoard)

            else:
                for row in range(Board.getMinRowSize(board), Board.getMaxRowSize(board)+1):
                    for col in range(Board.getMinColSize(board), Board.getMaxColSize(board)+1):
                        if (Board.comaprePieceat(board,col,row, colour)):
                            temp=Player.checkMove(board,col, row)
                            for pos in temp:
                                Successors.append((col,row,pos[0],pos[1]))


        return Successors




    def minimax(newBoard,colour,oppo_colour, type):

        beta=math.inf
        bestVal=-math.inf
        bestState=None
        cord=Player.getSuccessors(newBoard, colour,"bs",type)

        count=0
        MaxCount=0
        #for every state call minimax on them
        for board in Player.getSuccessors(newBoard, colour,"boards", type):
            value = Player.min_value(board, 2, colour, oppo_colour , bestVal, beta, type)
            if (value > bestVal):
                MaxCount=count
                bestVal = value
                bestState = board

            count+=1
        #if its the placing phase place the piece on the best possible move
        if (type=="PP"):
            Board.placePiece(newBoard,cord[MaxCount][0], cord[MaxCount][1],colour)
        #if its the moving phase move the piece to the best possible position
        if (type=="MP"):
            Board.movePiece(newBoard,cord[MaxCount][0],cord[MaxCount][1],cord[MaxCount][2],cord[MaxCount][3])
        return cord[MaxCount]


    def max_value(newBoard, depth, colour, oppo_colour , alpha, beta, type):
        #if the depth reaches 2 then start evaluating each state
        if(depth==3):
            if (type=="PP"):
                return Evaluation.eval1(newBoard,colour,oppo_colour)
            else:
                return Evaluation.eval2(newBoard,colour,oppo_colour)
        v=-math.inf

        #for each of the states from the lower depth get the max value
        for b in Player.getSuccessors(newBoard, colour, "boards",type):

            v=max(v, Player.min_value(b, depth+1, colour, oppo_colour , alpha, beta, type))


            if (v > beta):
                return v
            alpha = max(alpha, v)
        return v


    def min_value(newBoard, depth,colour, oppo_colour , alpha, beta, type ):
        # if the depth reaches 2 then start evaluating each state
        if(depth==3):
            if (type=="PP"):
                return Evaluation.eval1(newBoard,colour,oppo_colour)
            else:
                return Evaluation.eval2(newBoard,colour,oppo_colour)

        v=math.inf
        # for each of the states from the lower depth get the min value
        for b in Player.getSuccessors(newBoard, oppo_colour, "boards", type):

            v=min(v, Player.max_value(b,depth+1,colour,oppo_colour, alpha, beta,type))
            if (v < alpha):
                return v
            beta = min(beta, v)
        return v

#action= argmax(getSuccessorsMP(newboard, colour), lambda(newBoard): min_value(newBoard))




    #this function goes through the board and places the particular piece at the first empty position it finds
    def placing_phase(board,colour):


        if(colour == "W"):
            for col in range (0,8):
                for row in range (0,6):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        Board.placePiece(board,col,row,"W")
                        return(col,row)
        if(colour == "B"):
            for col in range (0,8):
                for row in reversed(range (2,8)):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        Board.placePiece(board,col,row,"B")
                        return(col,row)

        return();

    def moving(board,colour):

        for col in range(0,8):
            for row in range(0,8):
                if (Board.comaprePieceat(board,col,row, colour)):
                    if Game.freeUp(board,col,row):
                        Board.movePiece(board,col,row,col,row-1)
                        return((col,row),(col,row-1))
                    if Game.freeDown(board,col,row):
                        Board.movePiece(board,col,row,col,row+1)
                        return((col,row),(col,row+1))
                    if Game.freeRight(board,col,row):
                        Board.movePiece(board,col,row,col+1,row)
                        return((col,row),(col+1,row))
                    if Game.freeLeft(board,col,row):
                        Board.movePiece(board,col,row,col-1,row)
                        return((col,row),(col-1,row))
        return()






    def action(self, turns):

        Game.removeKills(self.board)

        self.no_turns=turns
        self.our_turns+=1
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)
        if(self.our_turns==24):
            self.plasingPhase=False
            print("CHnaged to mving phase")



        if (self.plasingPhase):
            return(Player.minimax(self.board,self.team_colour,self.oppo_colour,"PP"))
            Board.printBoard(self.board)
            #Player.placing_phase(self.board, self.team_colour))

        else:
            print("My moving phase activated")
            out=Player.minimax(self.board,self.team_colour,self.oppo_colour, "MP")
            print(out)
            return(out[0],out[1]),(out[2],out[3])
            return Player.moving(self.board, self.team_colour)





    def update(self, action):
        Board.printBoard(self.board)
        self.no_turns=self.no_turns+1
        self.our_turns+=1
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)
        if(self.our_turns==24):
            self.plasingPhase=False
            print("CHnaged to mving phase")


        Game.removeKills(self.board)
        print(self.no_turns)
        print(action)

        if(self.plasingPhase):
            Board.placePiece(self.board,action[0],action[1],self.oppo_colour)
        else:
            Board.movePiece(self.board,action[0][0], action[0][1], action[1][0],action[1][1])
