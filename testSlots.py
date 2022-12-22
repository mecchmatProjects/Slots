#!/usr/bin/env python
# coding: utf-8

# In[58]:


import numpy as np
import numpy.random as rnd

COINS = {
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
  "Ftt":1.5,
  "GoldenBox":0
}

N = 5
GoldenBoxValue = 500


def generateProbs(values, q=0.4):
    print(values)
    probs = np.zeros(len(values))
    n = len(values)
    
    pie = q/n/GoldenBoxValue
    
    #probs[:-1] = np.power(pie, 1./5) 
    print(probs)
    
    ts = 0.2
    ss = 0
    for i in range(n-1):
        if values[i] * N > q: 
            probs[i] = 0.01
        else:
            ss += values[i]**(-3)
        #print(probs[i])
        ts += probs[i]
    
    # print(ts)
    probs[-1] = 0.2
    
    for i in range(n-1):
        if values[i] * N <= q: 
            probs[i] = (1-ts) * values[i]**(-3) /ss
    
    
    
    print(probs)
    return probs    


def generateValues(coin_values):
    print(coin_values)
    
    coin_prices = np.array([item for item in coin_values.values()])
    coin_names = np.array([item for item in coin_values.keys()])

    probs = generateProbs(coin_prices)        
    res = np.random.choice(coin_names,N,p=probs)
    return res
    


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

                
def testMonteCarlo(coin_values, n):

        winSum = 0
        
        for _ in range(n):
                state = generateValues(coin_values)
                print("a=", state)
                w = calculateWin(state, coin_values)
                print("w=",w)
                winSum += w
                
        return winSum
        
        
if __name__ == "__main__":

        n = 5000      
        w = testMonteCarlo(COINS,n)
        ratio = w/n
        print(f"result={ratio}")
       


# In[ ]:





# In[ ]:




