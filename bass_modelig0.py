import random as rnd

N = 10
M = 6

R_Max = 110

K_start = 3

REELS = []

WeenPrice = [rnd.randint(0,15) for _ in range(N)]

CascadeNumbers = [0,0,0,0,0,1,1,1,1,1,]

# fill the REELS
for i in range(M):
    reel = [ rnd.randint(0,N) for _ in range(R_Max)]
    REELS.append(reel)

# probabilities of i-th symbol have right connect on j-th reel
connects =[ [ [0 for i in range(4)] for _ in range(N+1)] for __ in range(M) ]

for i in range(M-1):
    
    for j1 in range(R_Max):
        for j2 in range(R_Max):
            if REELS[i][j1] == REELS[i+1][j2-1] or \
               REELS[i][j1] == REELS[i+1][j2] or \
               REELS[i][j1] == REELS[i+1][(j2+1)%R_Max]:

                symbol = REELS[i][j1]
                
                countSymb = 1
                
                while REELS[i][(j1+countSymb)%R_Max] == symbol:
                    countSymb += 1

                if i==M-2:
                    while REELS[i+1][(j1+countSymb)%R_Max] == symbol:
                        countSymb += 1
                        
                connects[i][symbol][countSymb%4] += 1 / R_Max**2 * (3*K_start-2)/3/K_start


print(connects)

## calculate wins
ween = 0

# probability of cascade
probCasc = 0

for symb in range(N):
    for reel in range(M-1):
        for cnt in range(4):
            ween += WeenPrice[symb] * cnt * connects[reel][symb][cnt]
            probCasc += CascadeNumbers[symb] * connects[reel][symb][cnt]


print("Winings 1", ween)
print("Cascade prob:",probCasc)

# probabilities of i-th symbol have right connect on j-th reel
connects2 =[ [ [0 for i in range(4)] for _ in range(N+1)] for __ in range(M) ]

K_start = 4

# shift counts calculations
for i in range(M-1):
    
    for j1 in range(R_Max):
        for j2 in range(R_Max):
            if REELS[i][j1] == REELS[i+1][j2] or \
               REELS[i][j1] == REELS[i+1][(j2+1)%R_Max] or \
               REELS[i][j1] == REELS[i+1][(j2+2)%R_Max]:

                symbol = REELS[i][j1]
                
                countSymb = 1
                
                while REELS[i][(j1+countSymb)%R_Max] == symbol:
                    countSymb += 1

                if i==M-2:
                    while REELS[i+1][(j1+countSymb)%R_Max] == symbol:
                        countSymb += 1
                        
                connects2[i][symbol][countSymb%4] += 1 / R_Max**2 * (3*K_start-2)/3/K_start

print(connects2)
diff = 0
for symb in range(N):
    for reel in range(M-1):
        for cnt in range(4):
            d = abs(connects[reel][symb][cnt] - connects2[reel][symb][cnt])
            #print(diff)
            diff += d

print(diff)

## calculate wins
ween2 = 0

# probability of cascade
probCasc2 = 0

for symb in range(N):
    for reel in range(M-1):
        for cnt in range(4):
            ween2 += WeenPrice[symb] * cnt * connects2[reel][symb][cnt]
            probCasc2 += CascadeNumbers[symb] * connects2[reel][symb][cnt]


print("Winings 2", ween2)
print("Cascade prob2:",probCasc2)




                
            
