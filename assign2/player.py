
# coding: utf-8
import math
import copy

from watchYourBack import Board
from watchYourBack import Game
from evaluationFunctions import Evaluation
import minimax
import strategy as strategies

#import os
#import psutil

##################MEM USAGE#############
#process = psutil.Process(os.getpid())
#print(process.memory_info()[0]/(float)(2**20))
###################

################################################################################
# PLAYER CLASS
################################################################################
class Player:

    global WHITE_PLAYER
    global BLACK_PLAYER
    WHITE_PLAYER="W"
    BLACK_PLAYER="B"

    board=Board()                           #our main board
    team_colour=None                        #our team colour
    oppo_colour=None                        #Opponent team colour
    placingPhase=True                       #if its still the placing phase
    no_turns=0                              #number of turns given by ref
    our_turns=-1                            #our count of turns
    attkStrat=None                          #attacking strategy
    defStrat=None                           #defending strategy
    godStrat=None                           #godMode strategy
    massacre=None                           #massacre strategy
    def __init__(self,colour):
        #initializing the team colour
        if (colour=="white"):
            self.team_colour=WHITE_PLAYER
            self.oppo_colour=BLACK_PLAYER
        else:
            self.team_colour=BLACK_PLAYER
            self.oppo_colour=WHITE_PLAYER
    
        #initialize the strategies
        self.attkStrat=strategies.StrategyHub(strategies.attackStrategy)
        self.defStrat=strategies.StrategyHub(strategies.defendStrategy)
        self.godModeStrat=strategies.StrategyHub(strategies.godMode)
        self.massacreStrat=strategies.StrategyHub(strategies.massacre)



###############################################################################

#DUMMY MOVES

#    #this function goes through the board and places the particular piece at

#the first empty position it finds
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
    
        #remove all the kills before starting
        Game.removeKills(self.board,  self.oppo_colour, self.team_colour)
        #update our number of turns
        self.no_turns=turns
        self.our_turns+=1
        #shrink the board if it reaches a set numbe rof turns
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)

        #if we moved into the moving place, note it
        if(self.our_turns==24):
            self.placingPhase=False

        #if its the placing phase
        if (self.placingPhase):


            #if we have out peices in the 4 middle squares, excecute the god mode strategy
            if(Evaluation.mainFourSquares(self.board,self.team_colour,self.
                                                            oppo_colour)==1):
                out=self.godModeStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"PP",self.no_turns)
                #remove kills after placing
                Game.removeKillsAfterAction(self.board, out[0],out[1],
                                            self.oppo_colour, self.team_colour)
                return(out)



            tempAdvantage=Evaluation.PeiceAdvantage(self.board,self.team_colour,
                                                                self.oppo_colour)
            #if we have 5 more peices than the opponent, massacre!!!!!!!
            if(tempAdvantage>=5):
                out=self.massacreStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"PP",self.no_turns)
                #remove kills after placing
                Game.removeKillsAfterAction(self.board, out[0],out[1],
                                            self.oppo_colour, self.team_colour)
                return(out)



            #if we have 3 or less less peices than the opponent, excecute the
            #defend strategy
            if (tempAdvantage<=-3):
                out=self.defStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"PP",self.no_turns)
                #remove kills after placing
                Game.removeKillsAfterAction(self.board, out[0],out[1],
                                            self.oppo_colour, self.team_colour)
                return(out)
            else:
                #if not just atttaaackkkkkkk!!!!!
                out=self.attkStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"PP",self.no_turns)
                #remove kills after placing
                Game.removeKillsAfterAction(self.board, out[0],out[1],
                                            self.oppo_colour, self.team_colour)
                return(out)


        else: #if its moving phase
            #if we have out peices in the 4 middle squares, excecute
            #the god mode strategy
            if(Evaluation.mainFourSquares(self.board,self.team_colour,
                                                        self.oppo_colour)==1):
                out=self.godModeStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"MP",self.no_turns)
                if (out!=None):
                    #remove kills after the move
                    Game.removeKillsAfterAction(self.board, out[2],out[3],
                                            self.oppo_colour, self.team_colour)
                    return(out[0],out[1]),(out[2],out[3])
                return(None)


            #get our advantage
            tempAdvantage=Evaluation.PeiceAdvantage(self.board,
                                            self.team_colour,self.oppo_colour)
            #if we have 5 more peices than the opponent, massacre!!!!!!!
            if(tempAdvantage>=5):
                out=self.massacreStrat.execute(self.board,self.team_colour,
                                        self.oppo_colour,"MP", self.no_turns)
                Game.removeKillsAfterAction(self.board, out[2],out[3],
                                            self.oppo_colour, self.team_colour)
                return(out[0],out[1]),(out[2],out[3])
            #if we have 3 or less less peices than the opponent, excecute the
            #defend strategy
            if (tempAdvantage<=-3):
                out=self.defStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"MP", self.no_turns)
            else:
                #if not just atttaaackkkkkkk!!!!!
                out=self.attkStrat.execute(self.board,self.team_colour,
                                            self.oppo_colour,"MP", self.no_turns)
            if (out!=None):
                #remove kills after the move
                Game.removeKillsAfterAction(self.board, out[2],out[3],
                                            self.oppo_colour, self.team_colour)
                return(out[0],out[1]),(out[2],out[3])
            return(None)





    def update(self, action):
        #update number of turns
        self.no_turns=self.no_turns+1
        self.our_turns+=1
        #shrink board when number of turns achived
        if(self.no_turns==128):
            Game.shrinkBoard(self.board)
        if(self.no_turns==192):
            Game.shrinkBoard(self.board)
        if(self.our_turns==24):
            self.placingPhase=False

        #remove kill before anything
        Game.removeKills(self.board, self.team_colour, self.oppo_colour)
        if (action != None):
            #if its the placing phase
            if(self.placingPhase):
                #after placing the peice check for kills
                Board.placePiece(self.board,action[0],action[1],self.oppo_colour)
                Game.removeKillsAfterAction(self.board, action[0], action[1],
                                            self.team_colour, self.oppo_colour)
            else:
                #after moivng check for kills
                Board.movePiece(self.board,action[0][0], action[0][1],
                                                    action[1][0],action[1][1])
                Game.removeKillsAfterAction(self.board, action[1][0],
                                action[1][1], self.team_colour, self.oppo_colour)
