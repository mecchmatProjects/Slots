from unittest import TestCase, main

from Bandit import OneHandBandit
from CustomExceptions import *


class OneHandBanditTest(TestCase):
    def setUp(self):
        self.banditObj = OneHandBandit(3, 3, 8)

    def test_setWinningCombs(self):
        combs = {(7, 7, 7): 100, (3, 5, 7): 200, (4, 3, 0): 500}
        self.banditObj.setWinningCombs(combs)
        # combs[(4,3,0)] = 5
        self.assertDictEqual(combs, self.banditObj.combinations)

    def test_setWinningCombs_exception_0(self):
        with self.assertRaises(CombinationLengthException):
            self.banditObj.setWinningCombs({(7, 7, 7): 100, (3, 5, 7): 200, (4, 3, 0, 0): 500})

    def test_setWinningCombs_exception_1(self):
        with self.assertRaises(CombinationValuesException):
            self.banditObj.setWinningCombs({(7, 7, 8): 100, (3, 5, 7): 200, (4, 3, 0): 500})

    def test_setWinningCombs_exception_2(self):
        with self.assertRaises(WinningMoneyException):
            self.banditObj.setWinningCombs({(7, 7, 7): -100, (3, 5, 7): 200, (4, 3, 0): 500})

    def test_addWinningComb(self):
        comb = (7, 7, 7)
        win = 1000
        self.banditObj.addWinningComb(comb, win)
        # win = 500
        self.assertEqual(self.banditObj.combinations[comb], win)

    def test_setPriceOfGame(self):
        price = 10
        self.banditObj.setPriceOfGame(price)
        self.assertEqual(self.banditObj.price, price)

    def test_startGame(self):
        money = 100
        self.banditObj.startGame(money)
        self.assertEqual(self.banditObj.money, money)

    def test_setProbabilities_NoneProbs(self):
        probs = None
        self.banditObj.setProbabilities(probs)
        self.assertListEqual(self.banditObj.probabilities,
                             [1 / self.banditObj.picturesNumb for _ in range(self.banditObj.picturesNumb)])

    def test_setProbabilities(self):
        probs = [0.1, ] * 7 + [0.3]
        self.banditObj.setProbabilities(probs)
        # probs[0] = 0.5
        self.assertListEqual(list(self.banditObj.probabilities), probs)

    def test_setProbabilities_exception_0(self):
        probs = [0.1, ] * 7 + [0.4]
        with self.assertRaises(ProbabilitiesSumException):
            self.banditObj.setProbabilities(probs=probs)

    def test_setProbabilities_exception_1(self):
        probs = [0.1, ] * 8 + [0.2]
        with self.assertRaises(ProbabilitiesArrayLengthException):
            self.banditObj.setProbabilities(probs=probs)

    def test_setProbabilitiesFromTxtFile(self):
        filename = "tests/test_probabilities.txt"
        with open(filename, "r") as f:
            probs = list(map(float, f.readline().split(" ")))
        self.banditObj.setProbabilitiesFromTxtFile(filename)
        self.assertListEqual(probs, self.banditObj.probabilities)

    def test_setState_exception_0(self):
        state = [[1, 2, 3], [2, 3, 4], [3, 4, 3]]
        with self.assertRaises(SettingStateException):
            self.banditObj.setState(state)

    def test_turnColumn(self):
        turnColumn = self.banditObj.turnColumn(0)
        self.assertNotIn(-1, turnColumn)
        self.assertEqual(self.banditObj.rowsNumb, len(turnColumn))


if __name__ == '__main__':
    main()
