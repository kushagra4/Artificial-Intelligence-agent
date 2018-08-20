
# coding: utf-8
import math
import copy

######################################################
#class of Piece
#colour White(W) Black(B) Corner(X) Empty(E)
class Piece:
    colour=""
    def __init__(self, c):
        self.colour=c


######################################################
#Class of 8 X 8 board

class Board:

    def __init__(self):
        #starting and ending column numbers
        self.sCol=0
        self.eCol=7
        #starting and ending row numbers
        self.sRow=0
        self.eRow=7
        #setting the whole table as empty
        self.data = [[Piece("E")]*(self.eCol+1) for x in range(8)]
        #setting the cornr peices
        self.data[self.sCol][self.sRow]=Piece("X")
        self.data[self.eCol][self.sRow]=Piece("X")
        self.data[self.sCol][self.eRow]=Piece("X")
        self.data[self.eCol][self.eRow]=Piece("X")

    #printing the board just for checking
    def printBoard(board):
        for row in range(0,8):
            output=""
            for col in range(0,8):
                output=output+board.data[col][row].colour
            print(output)

    #place a peice of peice type in the board
    def placePiece(board,col, row, piece_type):
        board.data[col][row] = Piece(piece_type)

    #moving a peice on the board
    def movePiece(board, s_col,s_row,e_col,e_row):
        board.data[e_col][e_row]= Piece(board.data[s_col][s_row].colour)
        board.data[s_col][s_row]= Piece("E")

    #comparing if a peice of that colour is on a square
    def comaprePieceat(board, col,row,compColour):
        if (board.data[col][row].colour==compColour):
            return True
        return False

    #get the current minimum row size
    def getMinRowSize(board):
        return(board.sRow)
    #get the current max row size
    def getMaxRowSize(board):
        return board.eRow
    #get the current minimum col size
    def getMinColSize(board):
        return board.sCol
    #get the current max col size
    def getMaxColSize(board):
        return board.eCol
    #return if its a valid square
    def validSquare(board,col,row):
        if ((row>=board.sRow) and (row<=board.eRow) and  (col>=board.sCol) and (
                                                            col<=board.eCol)):
            return True
        return False
    #reducing the board size
    def reduceBoardSize(board):
            board.sCol=board.sCol+1
            board.eCol=board.eCol-1
            board.sRow=board.sRow+1
            board.eRow=board.eRow-1



######################################################
#fuction used to check an manipulate the board
class Game:
    #check if the square above is free
    def freeUp(board, col, row):
        if (Board.validSquare(board,col,row-1) and Board.comaprePieceat(board,
                                                            col,row-1, "E")):
            return True
        return False

    #check if the square below is free
    def freeDown(board,col, row):
        if (Board.validSquare(board,col,row+1) and Board.comaprePieceat(board,
                                                            col,row+1, "E")):
            return True
        return False

    #check if the square to the right is empty
    def freeRight(board, col, row):
        if (Board.validSquare(board,col+1,row) and Board.comaprePieceat(
                                                        board,col+1,row, "E")):
            return True
        return False

    #check if the square to the left it empty
    def freeLeft(board,col, row):
        if (Board.validSquare(board,col-1,row) and Board.comaprePieceat(
                                                        board,col-1,row, "E")):
            return True
        return False



################################################################################
    #checks if there is an enemy player or corner above the current square
    def checkUpKill(board,col,row, enemy):
        if (Board.validSquare(board,col,row-1) and ((Board.comaprePieceat(board,
            col,row-1, enemy) or (Board.comaprePieceat(board,col,row-1, "X"))))):
            return True
        return False
    #checks if there is an enemy player or corner below the current square
    def checkDownKill(board,col,row, enemy):
        if (Board.validSquare(board,col,row+1) and ((Board.comaprePieceat(board,
            col,row+1, enemy) or Board.comaprePieceat(board,col,row+1, "X")))):
            return True
        return False
    #checks if there is an enemy player or corner right of the current square
    def checkRightKill(board,col,row, enemy):
        if (Board.validSquare(board,col+1,row) and ((Board.comaprePieceat(board,
            col+1,row, enemy) or Board.comaprePieceat(board,col+1,row, "X")))):
            return True

        return False
    #checks if there is an enemy player or corner left of the current square
    def checkLeftKill(board,col,row, enemy):
        if (Board.validSquare(board,col-1,row) and ((Board.comaprePieceat(board,
            col-1,row, enemy) or Board.comaprePieceat(board,col-1,row, "X")))):
            return True
        return False

    #check if peice can be killed by an enemy
    def checkKill(board, col,row, enemy):
        return(((Game.checkUpKill(board,col,row, enemy)) and Game.checkDownKill(
            board,col,row, enemy)) or (Game.checkRightKill(board,col,row, enemy
            ) and Game.checkLeftKill(board,col,row, enemy)))


################################################################################
    #remove pieces after killing them from the board, fPrioirty: colour of the
    #last move sPrioirty: Other colour
    def removeKills(board, fPrioirty, sPrioirty):
        for col in range(0,8):
            for row in range(0,8):
                #checks items with prioirty first (eg item last placed)
                if(Board.comaprePieceat(board,col,row, sPrioirty)):
                    if Game.checkKill(board,col,row,fPrioirty):
                        Board.placePiece(board,col, row, "E")
                if(Board.comaprePieceat(board,col,row, fPrioirty)):
                    if Game.checkKill(board,col,row,sPrioirty):
                        Board.placePiece(board,col, row, "E")


################################################################################
    #checks if the peice moved or placed last affects any others and kill them if so.
    def removeKillsAfterAction(board, col, row, colour, oppo_colour):
        #check if it can kill peice above and kill it
        if (Board.validSquare(board,col,row-1) and (Board.comaprePieceat(board,
        col,row-1, colour)) and Game.checkKill(board, col, row-1,oppo_colour )):
            Board.placePiece(board,col, row-1, "E")
        #check if it can kill peice below and kill it
        if (Board.validSquare(board,col,row+1) and (Board.comaprePieceat(board,
        col,row+1, colour)) and Game.checkKill(board, col, row+1, oppo_colour)):
            Board.placePiece(board,col, row+1, "E")
        #check if it can kill peice left and kill it
        if (Board.validSquare(board,col-1,row) and (Board.comaprePieceat(board,
        col-1,row, colour)) and Game.checkKill(board, col-1, row,oppo_colour )):
            Board.placePiece(board,col-1, row, "E")
        #check if it can kill peice right and kill it
        if (Board.validSquare(board,col+1,row) and (Board.comaprePieceat(board,
        col+1,row, colour)) and Game.checkKill(board, col+1, row,oppo_colour )):
            Board.placePiece(board,col+1, row, "E")






    #shrinks the board by one size
    def shrinkBoard(board):
        #left down first
        for row in range(board.sRow,board.eRow+1):
            Board.placePiece(board,board.sRow, row, "-")
        #down right
        for col in range(board.sRow,board.eRow+1):
            Board.placePiece(board,col, board.eRow, "-")
        #right up
        for row in reversed(range(board.sRow, board.eRow+1)):
            Board.placePiece(board,board.eRow, row, "-")
        #up left
        for col in reversed(range(board.sRow,board.eRow+1)):
            Board.placePiece(board,col, board.sRow, "-")
        #reduce the board size
        Board.reduceBoardSize(board)
        #add the new corners and remove possible kills
        Board.placePiece(board,board.sRow,board.sRow,"X")
        Game.removeKillsAfterAction(board, board.sRow,board.sRow,"W","B")
        Game.removeKillsAfterAction(board, board.sRow,board.sRow, "B", "W")
        Board.placePiece(board,board.sRow,board.eRow,"X")
        Game.removeKillsAfterAction(board, board.sRow,board.eRow, "W","B")
        Game.removeKillsAfterAction(board, board.sRow,board.eRow, "B", "W")
        Board.placePiece(board,board.eRow,board.eRow,"X")
        Game.removeKillsAfterAction(board, board.eRow,board.eRow, "W","B")
        Game.removeKillsAfterAction(board, board.eRow,board.eRow,"B", "W")
        Board.placePiece(board,board.eRow,board.sRow,"X")
        Game.removeKillsAfterAction(board, board.eRow,board.sRow, "W","B")
        Game.removeKillsAfterAction(board, board.eRow,board.sRow, "B", "W")



        #remove if there are any kills
        Game.removeKills(board, "W", "B")
