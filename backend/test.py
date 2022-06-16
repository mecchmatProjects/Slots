import time

from backend.Bandit import OneHandBandit
import numpy as np
import matplotlib.pyplot as plt


def test1():
    """
    5 разів рахує ймовірності для
    двох заданих коефіцієнтів віддачі {0.9, 0.95};

    при різній кількості ігор: {1000, 3000, 5000, 10000};

    при різних початкових ймовірностях: {для ймовірностей с дуже великим значенням фітнесу, для рандомних ймовірностей}.

    Записує час за який було обраховано кожний набір ймовірностей та коефіцієнт віддачі на цих ймовірностях,
    обрахованний на 20000 ігор.
    """
    p2 = OneHandBandit(4, 3, 5)
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)
    # p2.addWinningComb((1, 1, 2, 2), 15)
    # p2.addWinningComb((2, 2, 3, 3), 15)
    # p2.addWinningComb((3, 3, 4, 4), 15)
    np.random.seed(42)

    # print("\ngamesCount=", 1000, "----------------\n")
    # test11(p2, gamesCount=1000)
    #
    # print("\ngamesCount=", 3000, "----------------\n")
    # test11(p2, gamesCount=3000)
    #
    # print("\ngamesCount=", 5000, "----------------\n")
    # test11(p2, gamesCount=5000)

    print("\ngamesCount=", 10000, "---------------\n")
    test11(p2, gamesCount=10000)


def test11(bandit, gamesCount):
    print("\nstarts with bad values --------------\n")
    population = [[0.34620235, 0.07168648, 0.06275534, 0.51076111, 0.00859472],
                  [0.48455469, 0.29974074, 0.18556755, 0.02237517, 0.00776185],
                  [0.4076457, 0.24869838, 0.14315961, 0.03328834000000005, 0.16720797],
                  [0.15385934, 0.64327094, 0.14050975, 0.03888020000000005, 0.02347977],
                  [0.32335616, 0.08463666, 0.28513406, 0.04416111, 0.26271201],
                  [0.43279837, 0.25248431, 0.05619025, 0.2325301, 0.02599697], ]

    print("\ngoal value: 0.9\n")
    badFitnessVals = [bandit.genAlgo.fitness_func(i, 0.9, gamesCount=gamesCount) for i in population]
    print(f"{badFitnessVals=}")
    test12(bandit, 0.9, gamesCount, population=population)

    print("\ngoal value: 0.95\n")
    badFitnessVals = [bandit.genAlgo.fitness_func(i, 0.95, gamesCount=gamesCount) for i in population]
    print(f"{badFitnessVals=}")
    test12(bandit, 0.95, gamesCount, population=population)

    print("\nstart with random values ------------\n")
    print("\ngoal value: 0.9\n")
    test12(bandit, 0.9, gamesCount)

    print("\ngoal value: 0.95\n")
    test12(bandit, 0.95, gamesCount)


def test12(bandit, goalValue, gamesCount, population=None):
    timeVals = []
    returnCoefVals = []
    for i in range(5):
        print(i, end=" ")
        t0 = time.time()
        probs = bandit.genAlgo.geneticAlgorithm(5, goalValue, population=population, gamesCount=gamesCount, )
        dt = time.time() - t0
        timeVals.append(dt)
        returnCoefVals.append(bandit.getReturnCoefWithNCores(gamesCount=20000, probs=probs))

    timeVals = np.array(timeVals)
    returnCoefVals = np.array(returnCoefVals)
    print("For 200 iterations:")
    print(f"min time: {min(timeVals)}, max time: {max(timeVals)}, mean time: {timeVals.mean()}")
    print(f"{timeVals=}")
    print(f"min returnCoefVals: {min(returnCoefVals)}, max returnCoefVals: {max(returnCoefVals)}, "
          f"mean returnCoefVals: {returnCoefVals.mean()}")
    print(f"{returnCoefVals=}")


def test2():
    """
    малює графік збіжності коефіцієнту віддачі автомата до певного числа при збільшенні номера гри
    """
    p2 = OneHandBandit(4, 3, 5)
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)

    # np.random.seed(42)
    # probs = p2.genBaseProbabilities(5, 0.9, debug=True)
    # print(f"{probs=}")
    # print("fitness val for probs and goalValue=0.9:", p2.genAlgo.fitness_func(probs=probs, goalValue=0.9))
    # print("return coef (goalValue):", p2.getReturnCoefWithNCores(probs=probs, gamesCount=10 ** 4))
    probs = [0.81674399, 0.10322578, 0.06974247, 0.0050837, 0.00520406]
    # gamesCount = 5000
    # meanRCs = p2.getReturnCoef(probs=probs, gamesCount=gamesCount, isGraph=True)
    # plt.plot(list(range(1, gamesCount + 1)), meanRCs)
    # plt.xlabel("Номер гри")
    # plt.ylabel("Коефіцієнт віддачі")
    # plt.plot([0, gamesCount], [0.9, 0.9], color="yellow")
    # plt.annotate("0.9", (gamesCount - 5, 0.9))
    #
    # plt.plot([gamesCount - 10, gamesCount - 10], [0.9, meanRCs[-1]], color="red")
    # plt.annotate(f"differance={round(abs(0.9 - meanRCs[-1]), 4)}", (gamesCount - 2 * 10 ** 3, 0.8))
    # plt.show()

    gamesCount = 20000
    meanRCs = p2.getReturnCoef(probs=probs, gamesCount=gamesCount, isGraph=True)
    plt.plot(list(range(1, gamesCount + 1)), meanRCs)
    plt.xlabel("Номер гри")
    plt.ylabel("Коефіцієнт віддачі")
    plt.plot([0, gamesCount], [0.9, 0.9], color="yellow")
    plt.annotate("0.9", (gamesCount - 5, 0.9))

    plt.plot([gamesCount - 10, gamesCount - 10], [0.9, meanRCs[-1]], color="red")
    plt.annotate(f"differance={round(abs(0.9 - meanRCs[-1]), 4)}", (gamesCount - 2 * 10 ** 3, 1))
    plt.show()


def test3():
    """
    функція, яка малює графік роботі генетичного алгоритму
    """
    p2 = OneHandBandit(4, 3, 5)
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)
    returnCoef = 0.95
    returnCoefsInGenerations = p2.genAlgo.geneticAlgorithm(p2.picturesNumb, returnCoef, isGraph=True, debug=True)
    plt.ylabel("коефіцієт віддачі")
    plt.xlabel("покоління")
    xs = [i * (len(returnCoefsInGenerations[0]) + 3) - 6 for i in range(1, len(returnCoefsInGenerations) + 1)]
    labels = list(range(len(returnCoefsInGenerations)))
    plt.xticks(xs, labels)
    plt.plot([0, len(returnCoefsInGenerations) * (len(returnCoefsInGenerations[0]) + 3)], [returnCoef, returnCoef],
             color="red")


    for idx, returnCoefs in enumerate(returnCoefsInGenerations):
        plt.plot([(len(returnCoefs) + 3) * idx + i for i in range(len(returnCoefs))], returnCoefs, "*")
        x0 = (len(returnCoefs) + 3) * idx + len(returnCoefs) + 1
        plt.plot([x0, x0], [0, 1], color="green")

    plt.show()

def test4():
    """
    функція, яка рахує та записує час на виконання функції обрахунку коефіцієнта віддачі
    та записує сам результат виконання,
    а потім каже про максимальні та мінімальні значення отриманих вибірок
    """
    p2 = OneHandBandit(4, 3, 5)
    p = p2.genBaseProbabilities(5)
    p2.setProbabilities(p)
    p2.setPriceOfGame(10)
    p2.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    p2.addWinningComb((4, 4, 4, 4), 15)


    l = []
    rcs = []
    modelingGamesCount = 10000
    coresCount = 0

    for i in range(100):
        t0 = time.time()
        returnCoef = p2.getReturnCoefWithNCores(gamesCount=modelingGamesCount, coresCount=coresCount)
        l.append(time.time() - t0)
        rcs.append(returnCoef)
        print(f"{i}) this one hand bandit return coefficient: {returnCoef} "
              f"for {modelingGamesCount} games"
              f"using {l[-1]} secs")
    print("min max time:", min(l), max(l))
    print("min max min_max_diff returnCoef:", min(rcs), max(rcs), max(rcs) - min(rcs))


if __name__ == '__main__':
    # test1()
    # test2()
    # test3()
    test4()