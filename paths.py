#!usr/bin/python env 

from collections import Counter

degrees = Counter({})

WIDTH = 6
HEIGHT = 3

def dfs2(W,H, x0,y0,d,path=[]):

	global degrees
	steps = ((0,1), (1,1), (1,0), (1,-1), (0,-1),(-1,-1),(-1,0),(-1,1))
	
	# print("xy",x0,y0)
	v = W*y0 + x0
	path.append(v) 
	if len(path)==d: 
		# print("path f:",path)
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
		dfs2(W,H,x1,y1,d,path)
		path.pop(-1)
				  		

dfs2(6,3,0,0,2,[])
print(degrees)

degrees.clear()

FNAME = "Coefs.txt"
f = open(FNAME,"w")


for i in range(WIDTH):
        for j in range(HEIGHT):
                dfs2(WIDTH,HEIGHT,i,j,4,[])
                # delete C^{d-1}_{d}?
                print(degrees, file=f)
                degrees.clear() # = Counter({})
                
                
f.close()



