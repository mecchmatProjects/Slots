
import numpy as np

class OneHandBandit:
	"""
	 There are m*n slots(columns,row)
	and k pictures for each slot(column)
	Pictures represented as integers 0..k-1
	 (You can create visuals by setting them to real image files)
	"""

	def __init__(self, m, n ,k):
		self.drumsColumns = [ [i for i in range(k)] for _ in range(m)]
		self.column = m
		self.row = n
		# maybe not in constructor???
		self.state = self.displayCurrentTurn()

		# price of the 1 turn of game???


	# winning combinations input
	# combinations like [7,7,7]:100$, [3,5,7]:200$, ['king','king','king']:500$ etc
	def setWinningCombs(combs):
		self.combinations = combs

	def addWinningCombs(comb,win):
		self.combinations[combs] = win

	# the price of 1 turn 		 
	def setPriceOfGame(price):
		self.price = price

	# money player gives to bandit
	def startGame(money):
		self.money
	# methods to good display of games...


	# Here is the trickiest part
	# we want to differ pribabilities of images
	# on each column and row
	def _setProbabilties(***)
		self.probs =[[]] #****

	# randomly display n*m result of turn
	def currentTurn():
		
		self.state = [turnColumn(i) for i in range(m)]
		return self.state

	# this methods could be with further changes....
	# our probalities are not necessary uniform!!!!
	# get random i-th column 
	# TODO: generalize and modify this!!!
	#!!! U should implement different options for this method...
	def turnColumn(i):
		# get n images from k without dublicates
		# easy uniform probability form
		# could be kept for testing
		# but more complex form also implemented
		return np.random.randint(1,k,n)



	# TODO: return i-th row
	def getRow(i):
		pass

	def getColumn:
		return self.state[i]
	 
	# TODO: display to user result
	def printState:
		pass

	# getters ..setters
	def getState():
		return self.state



	def currentWin():
		win = 0
		for i in range(self.row):
			if getRow(i) in self.combinations:
				# it is possible to have several winning combinations....
				win += self.combinations[getRow(i)]

		self.money += win # ???? not sure if it is needed
		return win

	# number of turns
	def play(n):
		if self.money<self.price*n:
			print("Not enough money")
			return None
		pass # play game n times

	# winning sum in fact could be (and often is) negative ;-))
	def currentPlayerWin():
		return self.money # not sure

	def totalPlayerWin():
		pass

	# Our main goal
	# !! modification needed
	def getWinCoef():
		return moneyWon/moneySpent


	
