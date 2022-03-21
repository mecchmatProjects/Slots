from __future__ import annotations

from typing import Dict, Tuple, List
import numpy as np


class OneHandBandit:
    """
     There are m*n slots(columns,row)
    and k pictures for each slot(column)
    Pictures represented as integers 0..k-1
     (You can create visuals by setting them to real image files)
    """
    players: List[OneHandBandit] = []

    def __init__(self, m: int, n: int, k: int):
        """
        m: number of columns
        n: number of rows
        k: number of pictures

        """
        # todo: не дуже розумію де має використовуватись змінна drumsColumns
        self.drumsColumns = [[i for i in range(k)] for _ in range(m)]
        self.columnsNumb = m
        self.rowsNumb = n
        self.picturesNumb = k

        self.combinations: Dict[Tuple[int, ...], int] = dict()
        self.price: int = 0

        self.money: int = 0
        self.moneySpent = 0
        self.moneyWon: int = 0

        # maybe not in constructor???
        # old code string: self.state = self.displayCurrentTurn()
        self.state: np.array = np.array([])

        OneHandBandit.players.append(self)

    # price of the 1 turn of game???

    # winning combinations input
    # combinations like (7,7,7):100$, (3,5,7):200$, ('king','king','king'):500$ etc
    def setWinningCombs(self, combs: Dict[Tuple[int, ...], int]):
        """
        combs: dict of winning combinations
        example: { (7, 7, 7): 100, (3, 5, 7): 200, (4, 3, 0): 500 }
        """
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
    # todo: цей метод має просто встановлювати значення змінної money?
    def startGame(self, money: int) -> None:
        if money > 0:
            self.money = money
            print(f"you deposited {money} money")

    # methods to good display of games...

    # todo: я повинен сгенерувати ймовірності у цьому методі чи це просто сеттер
    #  та необхідно додатково написати метод генерующий ймовірності?
    # Here is the trickiest part
    # we want to differ probabilities of images
    # on each column and row
    def _setProbabilties(self):
        self.probs = [[]]  # ****

    # randomly display n*m result of turn
    def currentTurn(self) -> None:
        """
        return: np.array([np.array(dtype=int), ])
        example:
        np.array([np.array([0, 1, ... , self.picturesNumb-1]), ])
        """
        self.state = np.array([self.turnColumn(i) for i in range(self.columnsNumb)])
        self.money -= self.price
        self.moneySpent += self.price

        self.printState()

    # this methods could be with further changes....
    # our probalities are not necessary uniform!!!!
    # get random i-th column
    # TODO: generalize and modify this!!!
    # !!! U should implement different options for this method...
    def turnColumn(self, i) -> np.array:
        # get n(rowsNumb) images from k(picturesNumb) without duplicates
        # easy uniform probability form
        # could be kept for testing
        # but more complex form also implemented
        return np.random.randint(self.picturesNumb, size=self.rowsNumb)

    # TODO: return i-th row
    def getRow(self, i) -> np.array:
        return np.array([self.state[j, i] for j in range(self.columnsNumb)])

    def getColumn(self, j):
        return self.state[j]

    # TODO: display to user result
    def printState(self):
        print(f"current state: \n{self.state.T}")
        # print("money spent:", self.moneySpent)
        # print("money won:", self.moneyWon)
        print("money remained:", self.money)

    # getters ..setters
    def getState(self) -> np.array:
        return self.state

    def setState(self, state: np.array) -> None:
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
    def play(self, n):
        if self.money < self.price * n:
            print("Not enough money")
            return None
        # play game n times
        for _ in range(n):
            self.currentTurn()
            won = self.currentWon()
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
    # todo: не розумію як я маю по іншому описати цю функцію
    def getWinCoef(self):
        return self.moneyWon / self.moneySpent


class SettingStateException(Exception):
    def __str__(self):
        return "invalid values for state massive: values in each row have to be distinct"


class SettingWinningCombinationsException(Exception):
    def __str__(self):
        return "invalid values for dict combinations:"


class CombinationLengthException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " key length of dict combinations have to equal number columns " \
                                   "of massive state in class OneHandBandit"


class CombinationValuesException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " key values of dict combinations have to be " \
                                   "lower than (picturesNumb - 1) in class OneHandBandit" \
                                   "and greater than 0"


class WinningMoneyException(SettingWinningCombinationsException):
    def __str__(self):
        return super().__str__() + " winning money have to be greater than 0"


if __name__ == "__main__":
    p1 = OneHandBandit(3, 3, 4)
    p1.setPriceOfGame(10)
    p1.setWinningCombs({(0, 0, 0): 15, (1, 1, 1): 15, (2, 2, 2): 15, (1, 2, 3): 20, })
    p1.addWinningComb((3, 3, 3), 15)
    p1.startGame(100)
    p1.play(10)

    print(f"{p1.currentPlayerWon=}")

    p2 = OneHandBandit(4, 3, 5)
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)
    p2.startGame(100)
    p2.play(10)

    print(f"{p2.currentPlayerWon=}")

    print(f"{p2.totalPlayersWon=}")
