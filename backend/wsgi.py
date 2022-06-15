from flask import Flask, Response

from backend.Bandit import OneHandBandit

app = Flask(__name__)

# відображення індексу картинки до назви картинки
dict_ = {0: "at_at",
         1: "c3po",
         2: "darth_vader",
         3: "death_star",
         4: "falcon",
         5: "r2d2"}

wastedMoney = 0
wonMoney = 0


@app.route("/getState", methods=["GET", ])
def getState():
    """
    обробляє запит сайту щодо даних: currentState, wonMoney, returnCoef
    Returns:
        об'єкт класу Response, який містить всі необхідні дані, а саме: currentState, wonMoney, returnCoef
    """
    global wastedMoney, wonMoney
    bandit.startGame(bandit.price)
    won = bandit.play(n=1)[0]

    wastedMoney = wastedMoney + bandit.price
    wonMoney = wonMoney + won
    returnCoef = (wonMoney / wastedMoney)
    print(wonMoney)
    print(wastedMoney)

    currentState = bandit.getState().T

    currentState = [dict_[int(i)] for i in currentState.flatten()]
    print(','.join(currentState) + ',' + str(won) + ',' + str(round(returnCoef, 4)))
    resp = Response(','.join(currentState) + ',' + str(won) + ',' + str(round(returnCoef, 4)))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


if __name__ == '__main__':
    bandit = OneHandBandit(4, 3, 5)

    # l = bandit.genBaseProbabilities(bandit.picturesNumb, returnCoef)
    # bandit.setProbabilities(l)
    bandit.setProbabilitiesFromTxtFile("probabilities.txt")

    bandit.setPriceOfGame(10)
    bandit.setWinningCombs({(0, 0, 0, 0): 15, (1, 1, 1, 1): 15, (2, 2, 2, 2): 15, (3, 3, 3, 3): 15, (1, 2, 3, 4): 20, })
    bandit.addWinningComb((4, 4, 4, 4), 15)

    app.run(debug=True, host="0.0.0.0")
