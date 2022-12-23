#!/usr/bin/env python
# coding: utf-8


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


def coinPie(x):
    
    s5 = x**5 * 100 * 5
    s4 = 5 * x**4 * (1-x) * 20 * 4 
    s3 = 10 * x**3 * (1-x)**2 * 10 * 3
    s2 = 10 * x**2 * (1-x)**3 * 4 * 2
    s1 = 5 * x * (1-x)**4
    
    return s1 + s2 + s3 + s4 + s5
    
    
def pltCp(h):
    
    x = 0 
    
    while x <1:
        x += h
        print(coinPie(x))
        
def findCoinPie(a,b,t,eps=0.000001):
    
    c = (a + b)/2
    
    if (b-a)<eps:
        return c
    
    if coinPie(c)>t:
        return findCoinPie(a,c,t,eps)
    return findCoinPie(c,b,t,eps)
    
    

def generateProbs(values, q=0.4):
    # print(values)
    probs = np.zeros(len(values))
    n = len(values)
    
    pie = q/n/GoldenBoxValue
    
    #probs[:-1] = np.power(pie, 1./5) 
    # print(probs)
    
    sum_prob = 0
    sum_out = 0
    for i in range(n-1):
        if values[i]  > 0.01: 
            v = findCoinPie(0,1,q/(4*n)/values[i])
            probs[i] = min(v,0.5)
            
            sum_out += coinPie(probs[i]) * values[i]

            #print(probs[i])
            sum_prob += probs[i]
    

    """
    for i in range(n-1):
        if values[i] * N <= q: 
            probs[i] = (1-ts) * values[i]**(-2) /ss
    
    """
    
    #print(probs)
    return q - sum_out, 1-sum_prob, probs    

def findFreeProb(a,b,value,sum_prob,min_price,gb_val,eps):
    
    c = (a + b)/2
    
    if (b-a)<eps:
        return c, sum_prob-c
    
    val = c**5 * gb_val + coinPie(sum_prob-c) * min_price
    
    #print("vc:",val,c,sum_prob-c)
    
    if val>value:
        return findFreeProb(a,c,value,sum_prob,min_price,gb_val,eps)
    return findFreeProb(c,b,value,sum_prob,min_price,gb_val,eps)



def generateRealProbs(coin_values):
     #print(coin_values)
    
    coin_prices = np.array([item if item>0 else 500 for item in coin_values.values()])
    coin_names = np.array([item for item in coin_values.keys()])

    s,t,probs = generateProbs(coin_prices) 
    
    print("p=",s,t)
    
    min_price = np.min(coin_prices)
    ind = np.argmax(coin_prices)
    print(min_price,ind)
    
    p,p1 = findFreeProb(0,t,s,t,min_price,GoldenBoxValue,0.000001)
    
    probs[-1] = p 
    probs[2] = p1
    print(probs)
    return probs

def generateValues(coin_values,probs):
    #coin_prices = np.array([item if item>0 else 500 for item in coin_values.values()])
    coin_names = np.array([item for item in coin_values.keys()])

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
            sumWin += 4 * coins_values[k] * 2
        elif v==3:
            sumWin += 10 * coins_values[k] * 3
        elif v==4: 
            sumWin += 20 * coins_values[k] * 4
        elif v==5:
            sumWin += 100 * coins_values[k] * 5
            if k=="GoldenBox":
                sumWin += GoldenBoxValue
    return sumWin

                
def testMonteCarlo(coin_values, n):

        winSum = 0
        
        probs = generateRealProbs(coin_values)
        print(probs)
        
        for _ in range(n):
                state = generateValues(coin_values,probs)
                print("a=", state)
                w = calculateWin(state, coin_values)
                print("w=",w)
                winSum += w
                
        return winSum
        
        
if __name__ == "__main__":

        n = 10   
        w = testMonteCarlo(COINS,n)
        ratio = w/n
        print(f"result={ratio}")
        
        #pltCp(0.01)
       


# In[ ]:
