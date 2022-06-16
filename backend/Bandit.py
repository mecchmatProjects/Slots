from __future__ import annotations

import os
import time
from multiprocessing import Pool
from typing import Dict, Tuple, List, Optional, Union
import numpy as np

from tqdm import tqdm

from backend.CustomExceptions import *
from backend.GenAlgorithm import GeneticAlgorithm


class OneHandBandit:
    """ """
    players: List[OneHandBandit] = []

    def __init__(self, m: int, n: int, k: int, probs: Optional[List[float, ...]] = None):
        """функція конструктор для класу OneHandBandit
        Args:
            m: number of columns
            n: number of rows
            k: number of pictures

                k(number of pictures) must be greater or equal to n(number of rows)

            probs: probability of each picture appearance
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

        self.state: List[List[int,],] = list()

        self.genAlgo = GeneticAlgorithm(self)

        OneHandBandit.players.append(self)

    def setWinningCombs(self, combs: Dict[Tuple[int, ...], int]):
        """функція, яка встановлює виграшні комбінації

        Args:
          combs: dict of winning combinations

            example: { (7, 7, 7): 100, (3, 5, 7): 200, (4, 3, 0): 500 }

        Returns:

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

    def addWinningComb(self, comb: Tuple[int, ...], win: int) -> None:
        """функція, яка додає одну виграшну комбінацію до списку виграшних комбінацій

        Args:
          comb: комбінація індексів зображень
          win: виграшна сума

        Returns:

        """
        self.combinations[comb] = win

    # the price of 1 turn
    def setPriceOfGame(self, price) -> None:
        """функція, яка встановлює вартість однієї гри

        Args:
          price: вартість однієї гри

        Returns:

        """
        self.price = price

    # money player gives to bandit
    def startGame(self, money: int, modeling: bool = False) -> None:
        """функція, яка вносить до автомату певну суму грошей, на які можна грати

        Args:
          money: сума грошей, яка вноситься до автомату
          modeling: параметр, який регулює інформативність функції

        Returns:

        """
        if money > 0:
            self.money = money
            if not modeling:
                print(f"you deposited {money} money")

    def setProbabilities(self, probs: Optional[List[float, ...]] = None) -> None:
        """функція, яка встановлює ймовірності для відповідних зображень з індексами від 0 до self.picturesNumb - 1,
        слідкуючи за тим, щоб сума ймовірностей була рівною одиниці

        Args:
          probs: ймовірності зображень

        Returns:

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

    def setProbabilitiesFromTxtFile(self, filename: str = "probabilities.txt") -> None:
        """функція, яка читає ймовірності з файлу, які розділені одним пробілом та визиває функцію self.setProbabilities

        Args:
          filename: ім'я файлу з ймовірностями

        Returns:

        """
        with open(filename, "r") as f:
            probsLine = f.readline()
            probs = list(map(lambda x: float(x), probsLine.split(" ")))

        self.setProbabilities(probs)

    def genBaseProbabilities(self, probsCount: int, returnCoef: Optional[float] = None,
                             debug: bool = False) -> List[float]:
        """функція, яка генерує список ймовірностей, сума яких рівна одиниці.

        Можлива генерація випадкових ймовірностей
        та генерація ймовірностей, які б задовольняли певний коефіцієнт віддачі автомату

        Args:
          probsCount: довжина списку ймовірностей
          returnCoef: коефіцієнт віддачі автомату, який має задовольняти ймовірностям

            якщо returnCoef is None, то генеруються випадкові ймовірності

            якщо returnCoef is not None, то генеруються ймовірності за допомогою генетичного алгоритму

          debug: параметр, який регулює інформативність функції

        Returns:
          згенерований список ймовірностей

        """
        probs = []
        if returnCoef is None:
            # generate random probabilities
            high = 1
            e = 0.25 * high

            for _ in range(probsCount - 1):
                probs.append(np.random.uniform(0, high - e))
                high -= probs[-1]
                e = 0.01 * high
            probs.append(high)
            return probs
        else:
            probs = self.genAlgo.geneticAlgorithm(probsCount=probsCount, goalValue=returnCoef, debug=debug)
            return probs

    def getReturnCoef(self, gamesCount: int = 10 ** 4, probs: Optional[List[float, ...]] = None,
                      isGraph: bool = False) -> Union[float, List[float]]:
        """функція, яка рахує коефіцієнт віддачі автомата, моделюючи методом Монте-Карло gamesCount ігор.

        функція рахує середній виграш гравця, протягом gamesCount ігор, та ділить його на ціну однієї гри

        Args:
          gamesCount: кількість ігор, які будуть промодельовані
          probs: ймовірності зображень, з якими буде проводитись кожна гра
          isGraph: параметр, який відповідає за надання функцією додаткових даних необхідних для створення графіку

        Returns:
            коефіцієнт віддачі автомату, якщо isGraph рівне False

            список коефіцієнтів віддачі автомату для кожної гри, якщо isGraph рівне True

        """
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
        meanRCs = self.play(gamesCount, modeling=modeling, isGraph=isGraph)
        gameReturn = self.moneyWon
        gameReturnPercentage = gameReturn / self.moneySpent
        if probs is not None:
            self.setProbabilities(oldProbs)
        self.moneyWon = oldMoneyWon
        self.moneySpent = oldMoneySpent
        if isGraph:
            return meanRCs

        return gameReturnPercentage

    def getReturnCoefWithNCores(self, gamesCount: int = 10 ** 3, probs: Optional[List[float, ...]] = None,
                                coresCount: int = -1):
        """функція, яка прискорює обчислення коефіцієнту віддачі автомату для великої кількості ігор,
        шляхом розпаралелювання роботи.

        функція запускає coresCount процесів, де виконуються функції self.getReturnCoef,
        але для меншого значення gamesCount, рівному gamesCount // coresCount.

        Args:
          gamesCount: кількість ігор, які будуть промодельовані
          probs: ймовірності зображень, з якими буде проводитись кожна гра
          coresCount: кількість процесів, які запустить дана функція

        Returns:
          коефіцієнт віддачі автомату

        """
        if coresCount == -1:
            coresCount = int(os.cpu_count() * 0.75)
            if coresCount == 0:
                coresCount = 1
        elif coresCount == 0:
            return self.getReturnCoef(gamesCount, probs)

        gamesCountList = [gamesCount // coresCount, ] * coresCount
        gamesCountList[-1] += (gamesCount - sum(gamesCountList))

        args = zip(gamesCountList, [probs, ] * len(gamesCountList), )
        # args = list(args)

        with Pool(processes=coresCount) as executor:
            results = executor.starmap(self.getReturnCoef, args)

        res = sum(results) / coresCount
        return res

    # @benchmark
    def currentTurn(self, modeling: bool = False) -> int:
        """функція, яка генерує матрицю однієї гри(складається з стовпців, кожен з яких містить в собі індекси зображень)
        та викликає функцію self.setState

        Args:
          modeling: параметр, який регулює інформативність функції

        Returns:
          виграш гравця

        """
        self.setState([self.turnColumn(i) for i in range(self.columnsNumb)])
        self.money -= self.price
        self.moneySpent += self.price
        won = self.currentWon()

        if not modeling:
            self.printState()

        return won

    def turnColumn(self, i) -> List[int,]:
        """функція, яка генерує один стовпець для майбутньої матриці однієї гри

        Args:
          i: індекс стовпця, який також відповідає індексу стовпця з self.drumColumns,
             де кожен стовпець містить індекси зображень, які взагалі можуть з'явитися в і-тому стовпці матриці однієї гри

        Returns:
          список індексів зображень

        """
        downIdx = self.rowsNumb - 1
        upIdx = 0
        rolledPicturesIdx = []
        resColumn = [-1, ] * self.rowsNumb
        for idx in range(self.rowsNumb):
            newProbs = self.genTurnProbabilities(rolledPicturesIdxs=rolledPicturesIdx)

            # assert abs(sum(newProbs) - 1) < 0.001

            rolledPicIdx = np.random.choice(self.drumsColumns[i], size=1, p=newProbs)[0]
            rolledPicturesIdx.append(rolledPicIdx)

            if (idx % 2) == 0:
                resColumn[downIdx] = rolledPicIdx
                downIdx -= 1
            else:
                resColumn[upIdx] = rolledPicIdx
                upIdx += 1

        return resColumn

    def genTurnProbabilities(self, rolledPicturesIdxs: List[int, ...]) -> List:
        """функція, яка обраховує ймовірності для зображень у автоматі при генерації одного стовпчика,
        точніше описано в файлі README.ipynb

        Args:
          rolledPicturesIdxs: зображення, які уже були згенеровані у рядках одного стовпчика

        Returns:
          значення ймовірностей для наступної генерації

        """
        newProbs = np.array(self.probabilities, dtype=float)
        divideCoeff = 1 - sum([self.probabilities[idx] for idx in rolledPicturesIdxs])
        newProbs[rolledPicturesIdxs] = 0.0
        newProbs = newProbs / divideCoeff
        return list(newProbs)

    def currentWon(self) -> int:
        """функція, яка аналізує поточну матрицю гри та повертає весь виграш гравця за поточну гру

        Args:

        Returns:
          весь виграш гравця

        """
        won = 0
        for i in range(self.rowsNumb):
            comb = tuple(self.getRow(i))
            if comb in self.combinations:
                # it is possible to have several winning combinations....
                won += self.combinations[comb]

        self.moneyWon += won  # ???? not sure if it is needed
        return won

    def getRow(self, i) -> np.array:
        """функція, яка повертає і-ий рядок матриці self.state(матриці однієї гри)

        Args:
          i: індекс рядка матриці гри

        Returns:
          список індексів зображень

        """
        return np.array([self.state[j][i] for j in range(self.columnsNumb)])

    def getColumn(self, j):
        """функція, яка повертаю j-ий стовпець матриці self.state(матриці однієї гри)

        Args:
          j: індекс стовпця матриці гри

        Returns:
          список індексів зображень

        """
        return self.state[j]

    def getState(self) -> np.array:
        """функція, яка повертає матрицю self.state(матрицю однієї гри)

        Args:

        Returns:
          транспонована(задля спрощення її відображення) матриця self.state

        """
        return np.array(self.state).T

    def setState(self, state: List[List[int,],]) -> None:
        """функція, яка встановлює матрицю однієї гри

        Args:
          state: матриця індексів зображень однієї гри

        Returns:

        """
        if all([len(col) == len(set(col)) for col in state]):
            self.state = state
        else:
            raise SettingStateException

    def printState(self) -> None:
        """функція, яка відображає матрицю поточної гри, весь виграш гравця, гроші, які у нього залишилися"""
        print(f"current state: \n{self.getState()}")
        # print("money spent:", self.moneySpent)
        print("money won:", self.moneyWon)
        print("money remained:", self.money)

    def play(self, n, modeling: bool = False, isGraph: bool = False) -> Union[Optional[List[int,]],
                                                                              List[float]]:
        """функція, яка проводить n ігор

        Args:
          n: кількість ігор
          modeling: параметр, який впливає на інформативність функції
          isGraph: параметра, який керує поверненням спеціальних значень

        Returns:
          список виграшів гравця за n ігор, якщо isGraph рівне False

          список коефіцієнтів віддачі автомату для кожної з n ігор, якщо isGraph рівне True

        """
        if self.money < self.price * n:
            print("Not enough money")
            return None

        wons = []
        meanRCs = []
        # play game n times
        for i in range(n):
            won = self.currentTurn(modeling=modeling)
            wons.append(won)
            if not modeling:
                print(f"you won {won} money for one turn")
                print(f"you spent {self.price} money for one turn")
                print()

            if isGraph:
                meanRCs.append(sum(wons) / ((i + 1) * self.price))

        if isGraph:
            return meanRCs

        if not modeling:
            return wons

    # winning sum in fact could be (and often is) negative ;-))
    @property
    def currentPlayerWon(self):
        """функція, яка декорується, як властивість об'єкту та повертає весь виграш гравця,
        віднявши від нього витрати гравця

        Args:

        Returns:
          виграш гравця - витрати гравця

        """
        return self.moneyWon - self.moneySpent  # not sure

    @property
    def totalPlayersWon(self):
        """функція, яка декорується, як властивість об'єкту та повертає весь виграш всіх гравців,
        який вона обраховує, використовуючи функцію self.currentPlayerWon

        Args:

        Returns:
          виграш всіх гравців - витрати всіх гравців

        """
        totalWin = 0
        for p in OneHandBandit.players:
            totalWin += p.currentPlayerWon
        return totalWin


if __name__ == "__main__":
    p2 = OneHandBandit(4, 3, 5)
    p2.setProbabilitiesFromTxtFile("probabilities.txt")

    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)

    # p2.startGame(100)
    # p2.play(10)
    try:
        returnCoef = float(
            input("write down return coefficient for probabilities you would like get for(Example 0.9): "))
    except Exception as e:
        print("during input error occurred:", e)
        print("return coefficient set to 0.9")
        returnCoef = 0.9
    # np.random.seed(42)
    probs = p2.genBaseProbabilities(p2.picturesNumb, returnCoef, debug=True)
    print(f"{probs=}")
    print(f"fitness val for probs and goalValue={returnCoef}:",
          p2.genAlgo.fitness_func(probs=probs, goalValue=returnCoef))
    print("return coef (goalValue):", p2.getReturnCoefWithNCores(probs=probs, gamesCount=10 ** 4))

    probsStrs = " ".join(map(str, probs))
    with open("probabilities.txt", "w") as f:
        f.write(probsStrs)

# метод ньютона

# генетичний алгоритм(рандомна мутація)
