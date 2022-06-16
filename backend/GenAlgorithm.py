from typing import List, Iterable, Tuple, Union

import numpy as np
from scipy.stats import truncnorm
from tqdm import tqdm


class GeneticAlgorithm:
    """ """

    def __init__(self, bandit):
        from backend.Bandit import OneHandBandit
        self.bandit: OneHandBandit = bandit

    def geneticAlgorithm(self, probsCount: int, goalValue: float,
                         populationSize: int = 6, population: List[List[float]] = None, gamesCount: int = 10000,
                         generationsCount: int = 100, eps: float = 0.001, debug: bool = False,
                         isGraph: bool = False) -> np.array:
        """основний метод генетичного алгоритму, який який керує усіма іншими методами та повертає результат,
        в виді списка ймовірностей

        Args:
          probsCount: довжина списку ймовірностей, який ви хотіли б отримати
          goalValue: значення коефіцієнта віддачі, якого ви хотіли б досягти зі згенерованими ймовірностями
          populationSize: розмір популяції генетичного алгоритму
          population: список індивидів(списків з ймовірностями), які будуть використовуватись генетичним алгоритмом
          gamesCount: кількість ігор, для функції обрахунку коефіцієнту віддачі,
            яка надалі буде використовуватися функцією фітнесу(fitness_func)
          generationsCount: максимальна кількість поколінь після, якої зупиниться генетичний алгоритм
          eps: похибка, яку дозволяє поточний генетичний алгоритм:
            генетичний алгоритм зупиниться,
            якщо (коефіцієнт віддачі згенерованих ймовірностей) - goalValue буде менше за цю похибку)
          debug: параметр, який регулює інформативність алгоритму:

            якщо debug рівне False алгоритм не інформує про зміни в поколіннях

            якщо debug рівне True алгоритм інформує про зміни в поколіннях
          isGraph: параметр, який відповідає за надання функцією додаткових даних необхідних для створення графіку

        Returns:
          якщо isGraph рівне False: список ймовірностей,
            які мають коефіцієнт віддачі рівним goalValue з певною похибкою eps
          якщо isGraph рівне True: списки коефіцієнтів віддачі популяції у різних поколіннях

        """
        if population is None:
            population = []
            for _ in range(populationSize):
                population.append(np.array(self.bandit.genBaseProbabilities(probsCount)))

            # population = [[0.34620235, 0.07168648, 0.06275534, 0.51076111, 0.00859472],
            #               [0.48455469, 0.29974074, 0.18556755, 0.02237517, 0.00776185],
            #               [0.4076457, 0.24869838, 0.14315961, 0.03328834000000005, 0.16720797],
            #               [0.15385934, 0.64327094, 0.14050975, 0.03888020000000005, 0.02347977],
            #               [0.32335616, 0.08463666, 0.28513406, 0.04416111, 0.26271201],
            #               [0.43279837, 0.25248431, 0.05619025, 0.2325301, 0.02599697], ]
            #               [0.39709205, 0.23165409, 0.0515545 , 0.24932884, 0.07037052], ]
            # fitness coefs: 0.65333333, 0.677     , 0.80883333, 0.5645    , 0.81633333

            # population = [[0.13124844, 0.47042438, 0.0631639 , 0.26138892, 0.07377436],
            #               [0.0952308 , 0.65992553, 0.14414762, 0.03988682, 0.06080923],
            #               [0.43279837, 0.25248431, 0.05619025, 0.2325301 , 0.02599697],
            #               [0.26570799, 0.52636168, 0.11265015, 0.05940529, 0.03587489],
            #               [0.39709205, 0.23165409, 0.0515545 , 0.24932884, 0.07037052], ]
            # fitness coefs: 0.76933333, 0.56766667, 0.77983333, 0.72416667, 0.802

        # цільова функція(фітнес функція) чим менше значення, тим більша ймовірність виживання індивіда
        fitness = lambda probs: self.fitness_func(probs=probs, goalValue=goalValue, gamesCount=gamesCount,
                                                  debug=debug, isGraph=isGraph)

        fitnessVals = []
        returnCoefsInGenerations = []
        # if debug is True:
        #     iterator = range(generationsCount)
        # else:
        #     iterator = tqdm(range(generationsCount))

        # for generationIdx in tqdm(range(generationsCount)):
        for generationIdx in range(generationsCount):
            if debug is True:
                print("\n######################generation:", generationIdx)

            fitnessVals = np.array([fitness(ps) for ps in population])
            if isGraph is True:
                mass = fitnessVals.copy()
                fitnessVals = np.array([i[1] for i in mass])
                returnCoefsInGenerations.append([i[0] for i in mass])

            if debug is True:
                print(f"{fitnessVals=}\n")

            # Обчислення коефіцієнту виживання кожного індивіду
            surviveProbs = self.getSurviveProbs(fitnessVals)
            # print(f"{surviveProbs=}\n")

            # Перевірка умов зупинки Генетичного Алгоритму
            if any(fitnessVals <= eps):
                if debug is True:
                    print("\n-----------------fitness values to break cycle:", fitnessVals)
                break

            # Відбір
            population = self.selection(population, surviveProbs)

            # Схрещування
            population = self.crossOver(population)
            for idx in range(len(population)):
                self.changeProbs(population[idx])

            # Мутація
            # ймовірність мутації кожної особини
            mutateProb = 0.1
            for idx in range(len(population)):
                rNumb = np.random.choice([0, 1], size=1, p=[1 - mutateProb, mutateProb])[0]
                if rNumb:
                    self.mutatePerson(population[idx], indpb=1 / len(population[idx]), debug=debug)

        if isGraph is True:
            return returnCoefsInGenerations

        mass = sorted(list(zip(fitnessVals, range(len(fitnessVals)))), key=lambda x: x[0])
        population = [population[i[1]] for i in mass]
        return population[0]

    # @benchmark
    def fitness_func(self, probs: List[float,], goalValue: float, debug: bool = False, isGraph: bool = False,
                     gamesCount: int = 5000) -> Union[float, Tuple]:
        """функція обраховує значення функції фітнесу:
        чим значення коефіцієнту віддачі ймовірностей probs ближче до goalValue, тим значення фітнес функції менше
        і навпаки.

        Args:
          probs: ймовірності для яких необхідно порахувати значення фітнес функції
          goalValue: значення коефіцієнту віддачі при якому рахується значення фітнес функція
          debug: параметр, який регулює інформативність функції
          gamesCount: кількість ігор, для функції обрахунку коефіцієнту віддачі
          isGraph: параметр, який відповідає за надання функцією додаткових даних необхідних для створення графіку

        Returns:
          якщо isGraph рівне False: значення фітнес функції
          якщо isGraph рівне True: (коефіцієнт віддачі, значення фітнес функції)

        """
        currReturnCoef = self.bandit.getReturnCoefWithNCores(gamesCount=gamesCount, probs=probs, coresCount=-1)
        # print(f"\n{probs=}")
        if debug is True:
            print(f"currFitness={abs(currReturnCoef - goalValue)}")
            print(f"{currReturnCoef=}\n")
        if isGraph is True:
            return currReturnCoef, abs(currReturnCoef - goalValue)

        return abs(currReturnCoef - goalValue)

    def getSurviveProbs(self, fitnessVals: np.array(List[Iterable[float]])) -> np.array(List[Iterable[float]]):
        """функція обраховує ймовірність виживання кожної окремої особини з популяції

        Args:
          fitnessVals: список значень функції фітнесу особин для популяції

        Returns:
          список ймовірностей виживання особин з популяції, обрахованний на основі значень функції фітнесу

        """
        fitnessVals[fitnessVals == 0] = 0.000001

        invS = sum(1 / fitnessVals)
        surviveProbs = (1 / fitnessVals) / invS
        return surviveProbs

    def selection(self, population: List[np.array,], surviveProbs):
        """функція реалізовує відбір методом рулетки для генетичного алгоритму

        Args:
          population: поточна популяція
          surviveProbs: ймовірності виживання кожної особини з поточної популяції

        Returns:
          нова популяція, такого ж розміру, що і стара, але без відсіяних особин

        """
        #
        indices = list(np.random.choice(range(len(population)), size=len(population), p=surviveProbs))
        newPopulation = list(np.array(population)[indices])
        return newPopulation

    def crossOver(self, population):
        """функція формує сім'ї(списки по дві особини) з поточної популяції, які потім передає у функцію схрещування

        Args:
          population: поточна популяція

        Returns:
          нова популяція, такого ж розміру, як і  стара, але з особин утворених в результаті скрещювання

        """
        # len(population) повинно бути парним

        # N = (len(population) // 2) * 2
        N = len(population)
        families = [population[i: (i + 2)] for i in range(0, N, 2)]
        # if len(population) % 2 == 1:
        #     families.append([population[-1], population[0]])

        # ймовірність схрещування
        crossOverProb = 0.9
        successors = [self.getSuccessor(f, crossOverProb) for f in families]
        newPopulation = []
        for i in successors:
            newPopulation.extend(i)

        return newPopulation

    def getSuccessor(self, family: np.array(np.array(List[Iterable[float]])), crossOverProb: float):
        """функціє реалізує одноточкове схрещування для генетичного алгоритму

        Args:
          family: список з двох особин для схрещування
          crossOverProb: ймовірність скрещювання(досить велика ймовірність)

        Returns:
          повертає двох особин:

          якщо схрещування відбулось: повертаються нові особини, які є результатом скрещювання

          якщо схрещування не відбулось: повертаються батьки(список family)

        """
        parent1, parent2 = family
        gensCount = len(parent1)

        # low border is inclusive, high border is exclusive
        splitIdx = np.random.randint(1, gensCount)
        # Х.-батько: a1 | b1,c1,d1; Х.-мати: a2 | b2,c2,d2; Х.-нащадок: a1,b2,c2,d2
        successor1 = np.array(list(parent1[: splitIdx]) + list(parent2[splitIdx:]))

        # Х.-батько: a1 | b1,c1,d1; Х.-мати: a2 | b2,c2,d2; Х.-нащадок: a2,b1,c1,d1
        successor2 = np.array(list(parent2[: splitIdx]) + list(parent1[splitIdx:]))

        # low border is inclusive, high border is exclusive
        rIdx = np.random.choice([0, 1], size=1, p=[1 - crossOverProb, crossOverProb])[0]
        if rIdx == 1:
            self.changeProbs(successor1)
            self.changeProbs(successor2)
            return [successor1, successor2]
        else:
            return family

    def mutatePerson(self, person: np.array, indpb: float = 0.01, delta: float = 1, debug: bool = False) -> None:
        """функція реалізує мутацію певної особини для генетичного алгоритму,
        де новий мутований ген вибирається,
        як значення нормально розподіленої випадкової величини
        з середнім рівним значенню поточного гену та дисперсією рівною одиничці

        Args:
          person: особина, яка буде піддана мутації
          indpb: ймовірність мутації одного гена особини(однієї ймовірності)
          delta: максимальна різниця між поточним геном та мутованим
          debug: параметр, який регулює інформативність функції

        Returns:

        """

        def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
            """

            Args:
              mean:  (Default value = 0)
              sd:  (Default value = 1)
              low:  (Default value = 0)
              upp:  (Default value = 10)

            Returns:

            """
            return truncnorm(
                (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

        person0 = person.copy()
        for idx in range(len(person)):
            if np.random.uniform() <= indpb:
                if debug is True:
                    print("mutation of one gen in one person_________________")
                leftBorder = max(0, person[idx] - delta)
                rightBorder = min(1, person[idx] + delta)
                # newGenVal = random.triangular(leftBorder, rightBorder, random.gauss(person[idx], 1))
                newGenVal = get_truncated_normal(mean=person[idx], sd=1, low=leftBorder, upp=rightBorder).rvs()
                if debug is True:
                    print(f"old {person=}")
                    print(f"old gen:{person[idx]}, new gen:{newGenVal}\n")
                # newGenVal = np.random.uniform(low=leftBorder, high=rightBorder, size=1)[0]
                person[idx] = newGenVal
                self.changeProbs(person, indsNot2ch=[idx, ])

                if debug is True:
                    print(f"new {person=}\n")

                if any(person < 0):
                    print(f"{person0=}")
                    print(f"{person=}")

    def changeProbs(self, probs: np.array, eps: float = 0.0001, indsNot2ch: List[int] = None) -> None:
        """якщо indsNot2ch порожній,
        функція зменшує або збільшує кожну ймовірність з probs, для того, щоб сума була рівна 1

        якщо indsNot2ch не порожній,
        функція зменшує або збільшує всі ймовірності з probs, окрім тих ймовірностей,
        чиї індексі зазначені у списку indsNot2ch, для того, щоб сума була рівна 1

        Args:
          probs: масив ймовірностей
          eps: похибка, яку дозволяє функція
          indsNot2ch: список індексів ймовірностей, які не можна змінювати

        Returns:

        """
        sVal = probs.sum()
        value = abs(1 - sVal)

        if value < eps:
            maxElIdx = max(zip(range(len(probs)), probs), key=lambda x: x[1])[0]
            indices = list(range(len(probs)))
            indices.remove(maxElIdx)

            probs[maxElIdx] = (1 - probs[indices].sum())
            return

        if indsNot2ch is None:
            inds2ch = list(range(len(probs)))
        else:
            inds2ch = [i for i in range(len(probs)) if i not in indsNot2ch]

        if sVal > 1:
            self.decreaseProbs(probs, value, inds2ch)
        else:
            self.increaseProbs(probs, value, inds2ch)

        # для того, щоб прибрати відхилення суми від одиниці, яке менше за eps
        self.changeProbs(probs)

    def decreaseProbs(self, probs: np.ndarray, value, inds2ch: List[int]) -> None:
        """value не повинно бути більше за sum(probs)
        зменшуємо кожне число пропорційно:

        якщо індекс ймовірності знаходиться у списку inds2ch, то ймовірність не змінюється

        якщо індекс ймовірності p0 не належить списку inds2ch
        та ймовірність p0 становить 50% від суми всіх ймовірностей, то p0 зменшиться на 50% від числа value

        Args:
          probs: список ймовірностей
          value: значення на яке сумарно треба зменшити ймовірності
          inds2ch: список індексів ймовірностей, які не можна змінювати

        Returns:

        """
        s = sum(probs[inds2ch])
        percents = probs[inds2ch] / s
        percentVals = percents * value
        probs[inds2ch] = probs[inds2ch] - percentVals

    def increaseProbs(self, probs: np.ndarray, value, inds2ch: List[int]):
        """value не повинно бути більше за sum(probs)
        збільшуємо кожне число пропорційно:

        якщо індекс ймовірності знаходиться у списку inds2ch, то ймовірність не змінюється

        якщо індекс ймовірності p0 не належить списку inds2ch
        та ймовірність p0 становить 50% від суми всіх ймовірностей, то p0 збільшиться на 50% від числа value

        Args:
          probs: список ймовірностей
          value: значення на яке сумарно треба зменшити ймовірності
          inds2ch: список індексів ймовірностей, які не можна змінювати

        Returns:

        """
        s = sum(probs[inds2ch])
        percents = probs[inds2ch] / s
        percentVals = percents * value
        probs[inds2ch] = probs[inds2ch] + percentVals
