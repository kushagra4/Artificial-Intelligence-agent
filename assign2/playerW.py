
# coding: utf-8
import math
import copy

from watchYourBack import Board
from watchYourBack import Game
from evaluationFunctions import Evaluation
import minimax
import strategy as strategies




class Player:
    board=Board()
    team_colour=None
    oppo_colour=None
    placingPhase=True
    no_turns=0
    our_turns=-1
    attkStrat=None
    defStrat=None
    def __init__(self,colour):
        if (colour=="white"):
            self.team_colour="W"
            self.oppo_colour="B"
        else:
            self.team_colour="B"
            self.oppo_colour="W"

        self.attkStrat=strategies.StrategyHub(strategies.attackStrategy)
        self.defStrat=strategies.StrategyHub(strategies.defendStrategy)

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



###############################################################################

#DUMMY MOVES

#    #this function goes through the board and places the particular piece at the first empty position it finds
#    def placing_phase(board,colour):
#
#
#        if(colour == "W"):
#            for col in range (0,8):
#                for row in range (0,6):
#                    if (Board.comaprePieceat(board,col,row, "E")):
#                        Board.placePiece(board,col,row,"W")
#                        return(col,row)
#        if(colour == "B"):
#            for col in range (0,8):
#                for row in reversed(range (2,8)):
#                    if (Board.comaprePieceat(board,col,row, "E")):
#                        Board.placePiece(board,col,row,"B")
#                        return(col,row)
#
#        return();
#
#    def moving(board,colour):
#
#        for col in range(0,8):
#            for row in range(0,8):
#                if (Board.comaprePieceat(board,col,row, colour)):
#                    if Game.freeUp(board,col,row):
#                        Board.movePiece(board,col,row,col,row-1)
#                        return((col,row),(col,row-1))
#                    if Game.freeDown(board,col,row):
#                        Board.movePiece(board,col,row,col,row+1)
#                        return((col,row),(col,row+1))
#                    if Game.freeRight(board,col,row):
#                        Board.movePiece(board,col,row,col+1,row)
#                        return((col,row),(col+1,row))
#                    if Game.freeLeft(board,col,row):
#                        Board.movePiece(board,col,row,col-1,row)
#                        return((col,row),(col-1,row))
#        return()
###############################################################################








    def action(self, turns):

        Game.removeKills(self.board)

        self.no_turns=turns
        self.our_turns+=1
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)
        if(self.our_turns==24):
            self.placingPhase=False
            print("CHnaged to mving phase")



        if (self.placingPhase):
            return(self.attkStrat.execute(self.board,self.team_colour,self.oppo_colour,"PP"))


        else:
            print("My moving phase activated")
            out=self.attkStrat.execute(self.board,self.team_colour,self.oppo_colour,"MP")
            return(out[0],out[1]),(out[2],out[3])





    def update(self, action):
        Board.printBoard(self.board)
        self.no_turns=self.no_turns+1
        self.our_turns+=1
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)
        if(self.our_turns==24):
            self.placingPhase=False
            print("CHnaged to mving phase")


        Game.removeKills(self.board)
        print(self.no_turns)
        print(action)

        if(self.placingPhase):
            Board.placePiece(self.board,action[0],action[1],self.oppo_colour)
        else:
            Board.movePiece(self.board,action[0][0], action[0][1], action[1][0],action[1][1])
