# ==============================CS-199==================================
# FILE:			RandomAI.py
#
# AUTHOR: 		Justin Chung
#
# DESCRIPTION:	This file contains the RandomAI class. In this class,
#				the RandomAI agent will return a random move at every turn
#				of the game.
#
# NOTES: 		- DO NOT MAKE CHANGES TO THIS FILE.
# ==============================CS-199==================================

from AI import AI
from Action import Action
import secrets


class RandomAI ( AI ):
	
	def __init__(self, rowDimension, colDimension, totalMines, startX, startY):
		self.__rowDimension = rowDimension
		self.__colDimension = colDimension
		self.__moveCount = 0


	def getAction(self, number: int) -> "Action Object":
		while self.__moveCount < 5:
			action = AI.Action(secrets.SystemRandom().randrange(1, len(AI.Action)))
			x = secrets.SystemRandom().randrange(self.__colDimension)
			y = secrets.SystemRandom().randrange(self.__rowDimension)
			self.__moveCount += 1
			return Action(action, x, y)

		action = AI.Action(secrets.SystemRandom().randrange(len(AI.Action)))
		x = secrets.SystemRandom().randrange(self.__colDimension)
		y = secrets.SystemRandom().randrange(self.__rowDimension)

		return Action(action, x, y)
