#!usr/bin/python env 

from collections import Counter

degrees = Counter({})

WIDTH = 6
HEIGHT = 3

def dfs_for_area_rounds(W,H, x0,y0,d,path=[], have = []):

	global degrees
	steps = ((0,1), (1,1), (1,0), (1,-1), (0,-1),(-1,-1),(-1,0),(-1,1))
	
	# print("xy",x0,y0)
	v = W*y0 + x0
	path.append(v) 
	
	extra_connected = 0
	for cell1 in have:
        	for nb in steps:
                        x2 = cell1 % W + nb[0] 
                        y2 = cell1 // W + nb[1]
                        if y2*W+x2 in path:
                                extra_connected += 1
                                break
                    
	print(extra_connected)
	# print(path)
	# input()
	
	if len(path) + extra_connected == d : 
		print("path f:",path)
		vals = []
		for cell in path:
			for nb in steps:
				x1 = cell % W + nb[0] 
				y1 = cell // W + nb[1]
				
				if x1<0 or x1>=W or y1<0 or y1>=H:
					continue
				val = W * y1 + x1
				if val in path:
					continue
				if val in vals:
					continue
				if val in have:
					continue	
				vals.append(val)
		# degrees.append(len(vals))
		degrees.update([len(vals)])
		# print("v:",vals)
		return
	# print("s=",x0,y0,v, path)
	for nb in steps:
		x1 = x0 + nb[0]
		y1 = y0 + nb[1]
		if x1<0 or x1>=W or y1<0 or y1>=H:
			continue
		v1 = W*y1 + x1
		# print("v1",v1)
		if v1 in path:
			continue
		if v1 in have:
			continue	
		dfs_for_area_rounds(W,H,x1,y1,d,path,have)
		path.pop(-1)
				  		

dfs_for_area_rounds(6,3,0,0,2,[],[0,5])
print(degrees)

degrees.clear()

FNAME = "Coefs.txt"
f = open(FNAME,"w")

calcul = {}

for i in range(WIDTH):
        for j in range(HEIGHT):
                dfs_for_area_rounds(WIDTH,HEIGHT,i,j,4,[],[1])
                # delete C^{d-1}_{d}?
                print(degrees, file=f)
                calcul[(i,j)] = degrees
                degrees.clear() # = Counter({})
                
                
f.close()


def prob(p,q,degs,d):
        s = 0
        for k,v in degs.items():
                s += v * q**k
         
        return s*p**d                

P = 0.1
Q = 0.8
for i in range(WIDTH):
        for j in range(HEIGHT):
                deg = calcul[(i,j)]
                for d in range(4,8):
                        val = prob(P,Q,deg,d)/d
                        print(val)
                       
               
                



