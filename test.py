import numpy as np
import numpy.random as rnd

coin_values = {
  "Xrp":0.4,
  "Ada":0.31,
  "Shiba":0.00000914,
  "Doge":0.087,
  "Gala":0.025,
  "Sand":0.55,
  "Mana":0.39,
  "FTM":0.18,
  "Trx":0.05,
  "Eos":0.92,
  "Hbar":0.0492,
  "Ftt":1.5
  "GoldenBox":0
}

N = 5

GoldenBoxValue = 500

def generateValues(coin_values):

       probs = generateProbs(coin_values.values) 
       
       res = np.random.choice(vals.keys(),N,p=probs)


def calculateWin(coins, coins_values):

       assert len(coins)==5, "Incorrect output"
       
       dict_coins = {}
       
       for x in coins:
             if x in dict_coins:
                dict_coins[x] +=1
             else:
                dict_coins[x] = 1
                
       sumWin = 0
       for k,v in dict_coins.items():
                if v==1:
                        sumWin += coins_values[k]
                elif v==2:
                        sumWin += 4 * coins_values[k]
                elif v==3:
                        sumWin += 10 * coins_values[k]
                elif v==4:
                        sumWin += 20 * coins_values[k]
                elif v==5:
                        sumWin += 100 * coins_values[k]
                        if k=="GoldenBox":
                                sumWin += GoldenBoxValue
       
       return sumWin
                
                
def testMonteCarlo(n):

        winSum = 0
        
        for _ in range(n):
        
                a = generateValues(coin_values)
              
                w = calculateWin(a)
                
                winSum += w
                
        return winSum
        
        
if __name__ == "__main__":

        n = 10000
        
        w = testMonteCarlo(n)
        
        print(f"result={w}")
       
       
