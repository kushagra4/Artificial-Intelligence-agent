#gets a successors of the board
from watchYourBack import Board
from watchYourBack import Game
from evaluationFunctions import Evaluation
import math
import copy




################################################################################
# countMoves calculates all the possible moves a single piece can make and
#sums it up: for the moving phase
def checkMove(board, col, row):
    possibleMoves = []

    # Check up if its free above and in the board range
    if (Board.validSquare(board,col,row-1) and Board.comaprePieceat(board,
                                                            col,row - 1, "E")):
        possibleMoves.append([col,row-1])

    # Check up for a jump over another piece above
    elif (Board.validSquare(board,col,row-2) and not (Board.comaprePieceat(board,
                col,row - 1, "E")) and Board.comaprePieceat(board,col,row-2,"E")):
        possibleMoves.append([col,row-2])

    # Check down if its free below and in the board range
    if (Board.validSquare(board,col,row+1) and Board.comaprePieceat(board,col,
                                                                row + 1, "E")):
        possibleMoves.append([col,row+1])
    # Check down for a jump below over another piece
    elif (((Board.validSquare(board,col,row+2)) and not(Board.comaprePieceat(
board,col,row - 1, "E"))) and (Board.comaprePieceat(board,col,row + 2, "E"))):
        possibleMoves.append([col,row+2])

    # check left if its free to the left and in the board range
    if (Board.validSquare(board,col-1,row) and Board.comaprePieceat(board,
                                                            col-1, row, "E")):
        possibleMoves.append([col-1,row])
    # check left for a jump over another piece to the left
    elif ((Board.validSquare(board,col-2,row) and not(Board.comaprePieceat(board,
                                                        col-1,row, "E"))) and
                (Board.comaprePieceat(board,col-2,row, "E"))):
        possibleMoves.append([col-2,row])

    # check right if its free to the right and in the board range
    if (Board.validSquare(board,col+1,row) and (Board.comaprePieceat(board,
                                                            col+1,row, "E"))):
        possibleMoves.append([col+1,row])
    # check right for a jump over another piece to the right
    elif ((Board.validSquare(board,col+2,row) and not(Board.comaprePieceat(board,
                                                            col+1,row, "E")))
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
                    moves += countMoves(board,row, col)

    return moves

################################################################################
#returns the successors
#takes in the board
#boolean if we need cordinates
#which phase it is (moving or placing)
#opponent colour
################################################################################
def getSuccessors(board, colour, needCord, type, oppo_colour):

    Successors=[]
    cord=[]
    #if its the placing phase then get states for that phase
    if (type=="PP"):

        #if you want the board as the output
        if(colour == "W"):
            for col in range (0,8):
                for row in range (0,6):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        #make a copy of the board that will represent a new state
                        tempBoard=copy.deepcopy(board)
                        Board.placePiece(tempBoard,col,row,"W")
                        #check if after placing the piece there is something
                        # that can be eliminated from the board and remove it
                        #from the board
                        Game.removeKills(tempBoard, colour, oppo_colour)
                        Successors.append(tempBoard)
                        if (needCord):
                            cord.append((col, row))

        if(colour == "B"):
            for col in range (0,8):
                for row in range (2,8):
                    if (Board.comaprePieceat(board,col,row, "E")):
                        #make a copy of the board that will represent a new state
                        tempBoard=copy.deepcopy(board)
                        Board.placePiece(tempBoard,col,row,"B")
                        # check if after placing the piece there is something
                        # that can be eliminated from the board and remove it
                        #from the board
                        Game.removeKills(tempBoard, colour, oppo_colour)
                        Successors.append(tempBoard)
                        if (needCord):
                            cord.append((col, row))

    # if its in the moving phase then get states for that phase
    if (type=="MP"):
        #check all the possible moves peices of our colour can make and return states
        for row in range(Board.getMinRowSize(board), Board.getMaxRowSize(board)+1):
            for col in range(Board.getMinColSize(board), Board.getMaxColSize(board)+1):
                if (Board.comaprePieceat(board,col,row, colour )):
                    temp=checkMove(board,col, row)
                    for pos in temp:
                        #make a copy of the board that will represent a new state
                        tempBoard=copy.deepcopy(board)
                        #move the peice to the new location
                        Board.movePiece(tempBoard,col,row,pos[0],pos[1])
                        #remove kills
                        Game.removeKills(tempBoard, colour,oppo_colour )
                        Successors.append(tempBoard)
                        if (needCord):
                            cord.append((col,row,pos[0],pos[1]))

    return (cord,Successors)


################################################################################
#implementation of minimax using alpha beta pruning
def minimax(newBoard,colour,oppo_colour, type, evalWeights, cutOff):

    #initialize beta and other needed variables
    beta=math.inf
    bestVal=-math.inf
    bestState=None
    #get the first set of cordinates so we could return when we get the state
    #cord=getSuccessors(newBoard, colour,"bs",type, oppo_colour)

    count=0
    MaxCount=0
    #for every state call min_value on them
    #note:we are running 2 depth here itseldf
    cord, bds = getSuccessors(newBoard, colour,True, type, oppo_colour)
    for board in bds:
        #if we want depth 1
        if (cutOff==1):
            value=Evaluation.evalFinal(board,colour,oppo_colour, evalWeights)
        else:
            value = min_value(board, 2, colour, oppo_colour , bestVal, beta,
                                                    type, evalWeights, cutOff)
        #get the max value (max val)
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
        if(len(cord)==0):
            return None
        Board.movePiece(newBoard,cord[MaxCount][0],cord[MaxCount][1],
                                            cord[MaxCount][2],cord[MaxCount][3])
    return cord[MaxCount]

################################################################################
def max_value(newBoard, depth, colour, oppo_colour , alpha, beta, type, evalWeights, cutOff):
    #if the depth reaches 2 then start evaluating each state
    if(depth==cutOff):
            return Evaluation.evalFinal(newBoard,colour,oppo_colour, evalWeights)
    v=-math.inf

    #for each of the states from the lower depth get the max value
    temp, bds = getSuccessors(newBoard, colour,False , type, oppo_colour)
    for b in bds:

        v=max(v, min_value(b, depth+1, colour, oppo_colour , alpha, beta, type,
                                                        evalWeights, cutOff))


        if (v > beta):
            return v
        alpha = max(alpha, v)
    return v

################################################################################
def min_value(newBoard, depth,colour, oppo_colour , alpha, beta, type , evalWeights, cutOff):
    # if the depth reaches 2 then start evaluating each state
    if(depth==cutOff):
        return Evaluation.evalFinal(newBoard,colour,oppo_colour, evalWeights)
    v=math.inf
    # for each of the states from the lower depth get the min value
    temp, bds =getSuccessors(newBoard, oppo_colour, False, type, colour)
    for b in bds:

        v=min(v, max_value(b,depth+1,colour,oppo_colour, alpha, beta,type,
                                                        evalWeights, cutOff))
        if (v < alpha):
            return v
        beta = min(beta, v)
    return v
