from __future__ import annotations

from typing import Dict, Tuple, List, Optional, Union
import numpy as np
from CustomExceptions import CombinationLengthException, CombinationValuesException, WinningMoneyException, \
    ProbabilitiesSumException, ProbabilitiesArrayLengthException, SettingStateException


class OneHandBandit:
    """
     There are m*n slots(columns,row)
    and k pictures for each slot(column)
    Pictures represented as integers 0..k-1
     (You can create visuals by setting them to real image files)
    """
    players: List[OneHandBandit] = []

    def __init__(self, m: int, n: int, k: int, probs: Optional[List[float, ...]] = None):
        """
        m: number of columns
        n: number of rows
        k: number of pictures
        k(number of pictures) must be greater or equal to n(number of rows)
        """

        self.drumsColumns = [[i for i in range(k)] for _ in range(m)]
        self.columnsNumb = m
        self.rowsNumb = n
        self.picturesNumb = k

        self.probabilities: List[float, ...] = list()
        self.setProbabilities(probs)

        self.combinations: Dict[Tuple[int, ...], int] = dict()
        self.price: int = 0

        self.money: int = 0
        self.moneySpent = 0
        self.moneyWon: int = 0

        # maybe not in constructor???
        # old code string: self.state = self.displayCurrentTurn()
        self.state: List[List[int,],] = list()

        OneHandBandit.players.append(self)

    # price of the 1 turn of game???

    # winning combinations input
    # combinations like (7,7,7):100$, (3,5,7):200$, ('king','king','king'):500$ etc
    def setWinningCombs(self, combs: Dict[Tuple[int, ...], int]):
        """
        combs: dict of winning combinations
        example: { (7, 7, 7): 100, (3, 5, 7): 200, (4, 3, 0): 500 }
        """
        combs = combs.copy()
        for comb in combs:
            if len(comb) != self.columnsNumb:
                raise CombinationLengthException
            elif max(comb) > (self.picturesNumb - 1) or min(comb) < 0:
                raise CombinationValuesException
            elif combs[comb] < 0:
                raise WinningMoneyException

        self.combinations = combs

    def addWinningComb(self, comb: Tuple[int, ...], win: int):
        self.combinations[comb] = win

    # the price of 1 turn
    def setPriceOfGame(self, price):
        self.price = price

    # money player gives to bandit
    def startGame(self, money: int, modeling: bool = False) -> None:
        if money > 0:
            self.money = money
            if not modeling:
                print(f"you deposited {money} money")

    # methods to good display of games...

    # Here is the trickiest part
    # we want to differ probabilities of images
    # on each column and row
    def setProbabilities(self, probs: Optional[List[float, ...]] = None):
        f"""
        set probabilities({self.probabilities}) for corresponding pictures(with indices from 0 till {self.picturesNumb})
        , where sum of probabilities have to equal 1
        """
        if probs is None:
            # uniform distribution
            probs = [1 / self.picturesNumb for i in range(self.picturesNumb)]

        if 0.001 < abs(sum(probs) - 1.0):
            # sum of probs dont equal 1
            raise ProbabilitiesSumException

        if len(probs) != self.picturesNumb:
            raise ProbabilitiesArrayLengthException

        self.probabilities = probs.copy()

    def setProbabilitiesFromTxtFile(self, filename: str = "probabilities.txt"):
        f"""
        read probabilities from .txt file, where probabilities values delimit with one space, 
        then use {self.setProbabilities} function
        raise: 
        ValueError if probabilities values are not float
        """
        with open(filename, "r") as f:
            probsLine = f.readline()
            probs = list(map(lambda x: float(x), probsLine.split(" ")))

        self.setProbabilities(probs)

    def genTurnProbabilities(self, rolledPicturesIdxs: List[int, ...]) -> List:
        newProbs = np.array(self.probabilities, dtype=float)
        divideCoeff = 1 - sum([self.probabilities[idx] for idx in rolledPicturesIdxs])
        newProbs[rolledPicturesIdxs] = 0.0
        newProbs = newProbs / divideCoeff
        return list(newProbs)

    def genBaseProbabilities(self, coef: float):
        # todo: now
        #  не дуже розумію що мається на увазі під "рандомно генерувати ймовірності",
        #  не розумію як їх генерувати, в залежності від коефіцієнту віддачі ігрового автомата,
        #  не розумію, що означає (Монте-Карло) цилк гравця
        pass

    def getOneHandBanditReturn(self, gamesCount: int = 10 ** 4, probs: Optional[List[float, ...]] = None) \
            -> Tuple[int, float]:
        oldProbs = self.probabilities
        oldMoneySpent = self.moneySpent
        oldMoneyWon = self.moneyWon
        if probs is not None:
            self.setProbabilities(probs)
        self.moneyWon = 0
        self.moneySpent = 0

        money = self.price * gamesCount

        modeling = True
        self.startGame(money, modeling=modeling)
        self.play(gamesCount, modeling=modeling)
        gameReturn = self.moneyWon
        gameReturnPercentage = gameReturn / self.moneySpent
        if probs is not None:
            self.setProbabilities(oldProbs)
        self.moneyWon = oldMoneyWon
        self.moneySpent = oldMoneySpent

        return gameReturn, gameReturnPercentage

    # randomly display n*m result of turn
    def currentTurn(self, modeling: bool = False) -> int:
        """
        return: np.array([np.array(dtype=int), ])
        example:
        np.array([np.array([0, 1, ... , self.picturesNumb-1]), ])
        """
        self.setState([self.turnColumn(i) for i in range(self.columnsNumb)])
        self.money -= self.price
        self.moneySpent += self.price
        won = self.currentWon()

        if not modeling:
            self.printState()

        return won

    # this methods could be with further changes....
    # our probalities are not necessary uniform!!!!
    # get random i-th column
    # TODO: generalize and modify this!!!
    # !!! U should implement different options for this method...
    def turnColumn(self, i) -> List[int,]:
        # get n(rowsNumb) images from k(picturesNumb) without duplicates
        # easy uniform probability form
        # could be kept for testing
        # but more complex form also implemented
        downIdx = self.rowsNumb - 1
        upIdx = 0
        rolledPicturesIdx = []
        resColumn = [-1, ] * self.rowsNumb
        for idx in range(self.rowsNumb):
            newProbs = self.genTurnProbabilities(rolledPicturesIdxs=rolledPicturesIdx)

            assert abs(sum(newProbs) - 1) < 0.001

            rolledPicIdx = np.random.choice(self.drumsColumns[i], size=1, p=newProbs)[0]
            rolledPicturesIdx.append(rolledPicIdx)

            if (idx % 2) == 0:
                resColumn[downIdx] = rolledPicIdx
                downIdx -= 1
            else:
                resColumn[upIdx] = rolledPicIdx
                upIdx += 1

        return resColumn

    def getRow(self, i) -> np.array:
        return np.array([self.state[j][i] for j in range(self.columnsNumb)])

    def getColumn(self, j):
        return self.state[j]

    def printState(self):
        print(f"current state: \n{np.array(self.state).T}")
        # print("money spent:", self.moneySpent)
        print("money won:", self.moneyWon)
        print("money remained:", self.money)

    # getters ..setters
    def getState(self) -> np.array:
        return self.state

    def setState(self, state: List[List[int, ], ]) -> None:
        if all([len(col) == len(set(col)) for col in state]):
            self.state = state
        else:
            raise SettingStateException

    def currentWon(self) -> int:
        won = 0
        for i in range(self.rowsNumb):
            comb = tuple(self.getRow(i))
            if comb in self.combinations:
                # it is possible to have several winning combinations....
                won += self.combinations[comb]

        self.moneyWon += won  # ???? not sure if it is needed
        return won

    # number of turns
    def play(self, n, modeling: bool = False):
        if self.money < self.price * n:
            print("Not enough money")
            return None
        # play game n times
        for _ in range(n):
            won = self.currentTurn(modeling=modeling)
            if not modeling:
                print(f"you won {won} money for one turn")
                print(f"you spent {self.price} money for one turn")
                print()

    # winning sum in fact could be (and often is) negative ;-))
    @property
    def currentPlayerWon(self):
        return self.moneyWon - self.moneySpent  # not sure

    # todo: мається на увазі загальний виграш всіх гравців?
    @property
    def totalPlayersWon(self):
        totalWin = 0
        for p in OneHandBandit.players:
            totalWin += p.currentPlayerWon
        return totalWin

    # Our main goal
    # !! modification needed
    def getWinCoef(self):
        return self.moneyWon / self.moneySpent


if __name__ == "__main__":
    p1 = OneHandBandit(3, 3, 4, probs=[0.5, 0.2, 0.2, 0.1])
    p1.setPriceOfGame(10)
    p1.setWinningCombs({(0, 0, 0): 15, (1, 1, 1): 15, (2, 2, 2): 15, (1, 2, 3): 20, })
    p1.addWinningComb((3, 3, 3), 15)
    modelingGamesCount = 10 ** 4
    returnMoney, returnCoef = p1.getOneHandBanditReturn(gamesCount=modelingGamesCount)
    print(f"this one hand bandit return: {returnMoney} with return coefficient: {returnCoef} "
          f"for {modelingGamesCount} games")
    p1.startGame(100)
    p1.play(10)

    print(f"{p1.currentPlayerWon=}\n")

    # p2 = OneHandBandit(4, 3, 5, probs=[0.1, 0.1, 0.1, 0.1, 0.6])
    p2 = OneHandBandit(4, 3, 5)
    p2.setProbabilitiesFromTxtFile()
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)

    modelingGamesCount = 10 ** 4
    returnMoney, returnCoef = p1.getOneHandBanditReturn(gamesCount=modelingGamesCount)
    print(f"this one hand bandit return: {returnMoney} with return coefficient: {returnCoef} "
          f"for {modelingGamesCount} games")

    p2.startGame(100)
    p2.play(10)

    print(f"{p2.currentPlayerWon=}")

    print(f"{p2.totalPlayersWon=}")
